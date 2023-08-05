"""
Extensions to traitlets for compatibility with JSON Schema

The biggest difference between these trait types and the built-in trait types
is the addition of the ``undefined`` sentinel. Javascript has both a "null"
and an "undefined" marker, while Python uses "None" for both.

Additionally, these traits support validation keywords related to those
defined in the JSON Schema specification: http://json-schema.org.
The code here targets jsonschema draft 04.

Also provided are ``to_dict()`` and ``from_dict()`` methods, so that class
instances can be instantiated from and serialized to dictionaries of values.
"""
import copy
import json
import textwrap

import six
import traitlets as T
from traitlets.traitlets import class_of
from traitlets.utils.importstring import import_item

__jsonschema_draft__ = 4


class UndefinedTraitError(T.TraitError):
    """Exception to raise when a required trait is undefined"""
    pass


class UndefinedType(object):
    """A Singleton type to mark undefined traits"""
    __instance = None

    def __new__(cls, *args, **kwargs):
        if not isinstance(cls.__instance, cls):
            cls.__instance = object.__new__(cls, *args, **kwargs)
        return cls.__instance

    def __repr__(self):
        return "undefined"


undefined = UndefinedType()


class JSONHasTraits(T.HasTraits):
    """A version of HasTraits with a few extra features:

    - supports default member types
    - supports to_dict() method and from_dict() class method

    Example
    -------
    >>> class Foo(JSONHasTraits):
    ...     _additional_traits = [T.Integer()]
    ...     name = T.Unicode()
    >>> f = Foo(name="Guido", score=42)
    >>> f.set_trait('value', 100)
    >>> sorted(f.trait_names())
    ['name', 'score', 'value']
    """
    _additional_traits = True  # boolean, or length-1 list of trait type allowed
    _skip_on_export = []  # traits to skip when exporting to dictionary
    _required_traits = []  # traits required at export. If undefined, a traiterror will be raised
    _converter_registry = {}  # converter classes to use for to_dict, from_dict
    _trait_name_map = {}  # mapping from trait names to schema names

    # Metadata is meant to hold top-level metadata keys used in JSON Schema,
    # for example '$schema' and/or '$id'
    _metadata = {'$schema': undefined, '$id': undefined}

    def __init__(self, **kwargs):
        # make a copy of the _metadata so we can modify locally
        self._metadata = self._metadata.copy()

        # Add default traits if needed
        default = self._get_additional_traits()
        # TODO: protect against overwriting class attributes defined above.
        #       perhaps use double underscores?
        if default:
            all_traits = self.traits()
            self.add_traits(**{key: default for key in kwargs
                               if key not in all_traits})

        # Validate keywords to make sure they are valid traits
        all_traits = list(self.traits())
        for k in kwargs:
            if k not in all_traits:
                raise T.TraitError("Invalid trait: {0}. Options for "
                                   "this class: {1}".format(k, all_traits))

        super(JSONHasTraits, self).__init__(**kwargs)

    def __contains__(self, key):
        return (key in self.traits() and
                getattr(self, key, undefined) is not undefined)

    def clone(self):
        """
        Return a clone of this object, recursively cloning each trait
        """
        def _clone(obj):
            if isinstance(obj, JSONHasTraits):
                return obj.clone()
            elif isinstance(obj, list):
                return [_clone(item) for item in obj]
            else:
                return obj

        kwds = {name: _clone(getattr(self, name))
                for name in self.trait_names()}
        return self.__class__(**kwds)

    @classmethod
    def _get_additional_traits(cls):
        try:
            default = cls._additional_traits[0]
        except TypeError:
            default = cls._additional_traits

        if isinstance(default, T.TraitType):
            return default
        elif default:
            return T.Any()
        else:
            return None

    @classmethod
    def register_converters(cls, **kwargs):
        cls._converter_registry.update(kwargs)

    def set_trait(self, name, value):
        default = self._get_additional_traits()
        if default and name not in self.traits():
            self.add_traits(**{name: default})
        super(JSONHasTraits, self).set_trait(name, value)

    @classmethod
    def from_dict(cls, dct, **kwargs):
        """Initialize an instance from a (nested) dictionary"""
        Visitor = cls._converter_registry.get('from_dict', FromDict)
        return Visitor().clsvisit(cls, dct, **kwargs)

    def to_dict(self, **kwargs):
        """Output a (nested) dict encoding the contents of this instance"""
        self._finalize(**kwargs)
        Visitor = self._converter_registry.get('to_dict', ToDict)
        return Visitor().visit(self, **kwargs)

    @classmethod
    def from_json(cls, json_string, json_kwds=None, **kwargs):
        """Instantiate object from a JSON string"""
        dct = json.loads(json_string, **(json_kwds or {}))
        return cls.from_dict(dct, **kwargs)

    def to_json(self, json_kwds=None, **kwargs):
        """Output the object's representation to a JSON string"""
        dct = self.to_dict(**kwargs)
        return json.dumps(dct, **(json_kwds or {}))

    def to_python(self, **kwargs):
        Visitor = self._converter_registry.get('to_python', ToPython)
        # Explicitly convert to str() for the sake of derived classes
        # which return a more complicated code representation object.
        return str(Visitor().visit(self, **kwargs))

    def __dir__(self):
        """Customize tab completed attributes."""
        traits = [t for t in self.traits() if t not in self._skip_on_export]
        return traits + ['to_dict', 'from_dict', 'to_json', 'from_json']

    def _finalize(self, *args, **kwargs):
        """Finalize the object, and all contained objects, for export."""
        def finalize_obj(obj):
            if hasattr(obj, '_finalize'):
                obj._finalize(*args, **kwargs)
            elif isinstance(obj, list):
                for item in obj:
                    # Note: *args, **kwargs are passed through the closure
                    finalize_obj(item)

        for name in self.traits():
            value = getattr(self, name)
            finalize_obj(value)


class AnyOfObject(JSONHasTraits):
    """A HasTraits class which selects any among a set of specified types"""
    _classes = []

    @classmethod
    def _class_defs(self):
        for cls in self._classes:
            if isinstance(cls, JSONInstance):
                cls = cls.klass
            if isinstance(cls, six.string_types):
                cls = import_item(cls)
            yield cls


    def __init__(self, *args, **kwargs):
        for cls in self._class_defs():
            # TODO: add a second pass where we allow additional properties?
            if all(key in cls.class_traits() for key in kwargs):
                try:
                    cls(*args, **kwargs)
                except (T.TraitError, ValueError):
                    pass
                else:
                    self.add_traits(**{key: copy.copy(val) for key, val
                                       in cls.class_traits().items()})
                    break
        else:
            raise T.TraitError("{cls}: initialization arguments not "
                               "valid in any wrapped classes"
                               "".format(cls=self.__class__.__name__))
        super(AnyOfObject, self).__init__(*args, **kwargs)


class OneOfObject(AnyOfObject):
    """A HasTraits class which selects any among a set of specified types"""
    # TODO: should specialize this so that exactly one of the objects matches
    pass


class AllOfObject(JSONHasTraits):
    """
    A HasTraits class which combines all properties of a set of specified types
    """
    # TODO: should we check whether additional traits pass additionalProperties
    # for each? This is required for full parity with JSONSchema
    _classes = []

    @classmethod
    def _class_defs(self):
        for cls in self._classes:
            if isinstance(cls, JSONInstance):
                cls = cls.klass
            if isinstance(cls, six.string_types):
                cls = import_item(cls)
            yield cls

    def __init__(self, *args, **kwargs):
        # TODO: handle _additional_traits
        all_traits = {}
        self._required_traits = []
        for cls in self._class_defs():
            all_traits.update(cls.class_traits())
            self._required_traits.extend(cls._required_traits)
        self.add_traits(**{name: copy.copy(trait) for name, trait
                           in all_traits.items()})
        super(AllOfObject, self).__init__(*args, **kwargs)


def AnonymousMapping(**traits):
    """Create an anonymous HasTraits mapping

    This is used when a JSONSchema defines an object inline, rather than in
    a separate statement

    Example
    -------
    >>> Foo = AnonymousMapping(val=T.Integer())
    >>> f = Foo(val=4)
    >>> type(f)
    <class 'traitlets.traitlets.AnonymousMapping'>
    """
    return T.MetaHasTraits('AnonymousMapping', (JSONHasTraits,), traits)


class JSONNull(T.TraitType):
    """A trait whose value can only be None"""
    allow_undefined = True
    default_value = undefined
    info_text = 'a JSON null value'

    def __init__(self, allow_undefined=True, **kwargs):
        self.allow_undefined = allow_undefined
        kwargs['allow_none'] = True
        super(JSONNull, self).__init__(**kwargs)

    def validate(self, obj, value):
        if self.allow_undefined and value is undefined:
            return value
        elif value is None:
            return value
        else:
            self.error(obj, value)


class JSONAny(T.Any):
    allow_undefined = True
    default_value = undefined
    info_text = 'any value'

    def __init__(self, allow_undefined=True, **kwargs):
        self.allow_undefined = allow_undefined
        super(JSONAny, self).__init__(**kwargs)

    def validate(self, obj, value):
        if value is undefined and not self.allow_undefined:
            self.error(obj, value)
        else:
            return value


def _validate_numeric(trait, obj, value,
                      minimum=undefined, maximum=undefined,
                      exclusiveMinimum=undefined, exclusiveMaximum=undefined,
                      multipleOf=undefined, **extra_kwds):
    if value is None:
        return value

    if minimum is not undefined:
        exclusive = exclusiveMinimum is not undefined and exclusiveMinimum
        if value < minimum or (exclusive and value == minimum):
            raise T.TraitError(
                "The value of the '{name}' trait of {klass} instance should "
                "not be less than {min_bound}, but a value of {value} was "
                "specified".format(
                    name=trait.name, klass=class_of(obj),
                    value=value, min_bound=minimum))

    if maximum is not undefined:
        exclusive = exclusiveMaximum is not undefined and exclusiveMaximum
        if value > maximum or (exclusive and value == maximum):
            raise T.TraitError(
                "The value of the '{name}' trait of {klass} instance should "
                "not be greater than {max_bound}, but a value of {value} was "
                "specified".format(
                    name=trait.name, klass=class_of(obj),
                    value=value, max_bound=maximum))

    if multipleOf is not undefined:
        if value % multipleOf != 0:
            raise T.TraitError(
                "The value of the '{name}' trait of {klass} instance should "
                "be a multiple of {multiple}, but a value of {value} was "
                "specified".format(
                    name=trait.name, klass=class_of(obj),
                    value=value, multiple=multipleOf))
    return value


class JSONNumber(T.Float):
    """A trait whose value is a JSON Number"""
    allow_undefined = True
    default_value = undefined
    info_text = "a JSON number"
    _validation_keywords = ["minimum", "maximum", "exclusiveMinimum",
                            "exclusiveMaximum", "multipleOf"]

    def __init__(self, allow_undefined=True, **kwargs):
        self.allow_undefined = allow_undefined
        self._validation_dict = {key: kwargs.pop(key)
                                 for key in self._validation_keywords
                                 if key in kwargs}
        super(JSONNumber, self).__init__(**kwargs)

    def validate(self, obj, value):
        if self.allow_undefined and value is undefined:
            return value
        value = super(JSONNumber, self).validate(obj, value)
        return _validate_numeric(self, obj, value, **self._validation_dict)


class JSONInteger(T.Integer):
    """A trait whose value is a JSON Integer"""
    allow_undefined = True
    default_value = undefined
    info_text = "a JSON integer"
    _validation_keywords = ["minimum", "maximum", "exclusiveMinimum",
                            "exclusiveMaximum", "multipleOf"]

    def __init__(self, allow_undefined=True, **kwargs):
        self.allow_undefined = allow_undefined
        self._validation_dict = {key: kwargs.pop(key)
                                 for key in self._validation_keywords
                                 if key in kwargs}
        super(JSONInteger, self).__init__(**kwargs)

    def validate(self, obj, value):
        if self.allow_undefined and value is undefined:
            return value
        value = super(JSONInteger, self).validate(obj, value)
        return _validate_numeric(self, obj, value, **self._validation_dict)


class JSONString(T.Unicode):
    """A trait whose value is a JSON string"""
    allow_undefined = True
    default_value = undefined
    info_text = "a JSON string"

    def __init__(self, allow_undefined=True, minLength=None, maxLength=None,
                 **kwargs):
        self.allow_undefined = allow_undefined
        self.minLength = minLength
        self.maxLength = maxLength
        super(JSONString, self).__init__(**kwargs)

    def _validate_string_length(self, obj, value):
        if self.minLength is not None and len(value) < self.minLength:
            raise T.TraitError(
                "The value of the '{name}' trait of {klass} instance should "
                "not be shorter than {minLength}, but a value of {value} was "
                "specified".format(
                    name=self.name, klass=class_of(obj),
                    value=value, minLength=self.minLength))

        if self.maxLength is not None and len(value) > self.maxLength:
            raise T.TraitError(
                "The value of the '{name}' trait of {klass} instance should "
                "not be longer than {maxLength}, but a value of {value} was "
                "specified".format(
                    name=self.name, klass=class_of(obj),
                    value=value, maxLength=self.maxLength))
        return value

    def validate(self, obj, value):
        if self.allow_undefined and value is undefined:
            return value
        value = super(JSONString, self).validate(obj, value)
        return self._validate_string_length(obj, value)


class JSONBoolean(T.Bool):
    """A trait whose value is a JSON boolean value"""
    allow_undefined = True
    default_value = undefined
    info_text = "a JSON boolean"

    def __init__(self, allow_undefined=True, **kwargs):
        self.allow_undefined = allow_undefined
        super(JSONBoolean, self).__init__(**kwargs)

    def validate(self, obj, value):
        if self.allow_undefined and value is undefined:
            return value
        return super(JSONBoolean, self).validate(obj, value)


class JSONUnion(T.Union):
    """A trait whose value matches one of a list of trait types"""
    allow_undefined = True
    default_value = undefined

    def __init__(self, trait_types, allow_undefined=True, **kwargs):
        self.allow_undefined = allow_undefined
        super(JSONUnion, self).__init__(trait_types, **kwargs)

    def validate(self, obj, value):
        if self.allow_undefined and value is undefined:
            return value
        return super(JSONUnion, self).validate(obj, value)


def _has_unique_elements(L):
    """Return True if all items in the list are unique"""
    # Hashable types
    try:
        S = set(L)
    except TypeError:
        pass
    else:
        return len(L) == len(S)

    # Unhashable but orderable types
    try:
        L = sorted(L)
    except TypeError:
        pass
    else:
        from itertools import groupby
        return len(L) == len([k for k, v in groupby(L)])

    # Unhashable, unorderable types
    return all(L[i] != L[j]
               for i in range(len(L))
               for j in range(i + 1, len(L)))


class JSONArray(T.List):
    """A trait whose value is an array of typed items"""
    allow_undefined = True
    default_value = undefined
    info_text = "an Array of values"

    def __init__(self, trait, allow_undefined=True,
                 uniqueItems=False, **kwargs):
        self.allow_undefined = allow_undefined
        self.uniqueItems = uniqueItems
        if 'minItems' in kwargs:
            kwargs['minlen'] = kwargs.pop('minItems')
        if 'maxItems' in kwargs:
            kwargs['maxlen'] = kwargs.pop('maxItems')
        super(JSONArray, self).__init__(trait, **kwargs)

    def validate(self, obj, value):
        if self.allow_undefined and value is undefined:
            return value
        value = super(JSONArray, self).validate(obj, value)
        if self.uniqueItems and not _has_unique_elements(value):
            raise T.TraitError(
                "The value of the '{name}' trait of {klass} instance should "
                "have unique elements".format(
                    name=self.name, klass=class_of(obj)))
        return value

    # Need to bypass the dynamic default in T.Container() in the case that
    # the trait is undefined
    def make_dynamic_default(self):
        if self.allow_undefined and self.default_value is undefined:
            return undefined
        else:
            return super(JSONArray, self).make_dynamic_default()


class JSONEnum(T.Enum):
    """A trait whose value is one of a specified list of options"""
    allow_undefined = True
    default_value = undefined
    info_text = "an enum of values"

    def __init__(self, values, allow_undefined=True, **kwargs):
        self.allow_undefined = allow_undefined
        super(JSONEnum, self).__init__(values, **kwargs)

    def validate(self, obj, value):
        if self.allow_undefined and value is undefined:
            return value
        return super(JSONEnum, self).validate(obj, value)


class JSONInstance(T.Instance):
    """A trait whose value is an instance of a class"""
    allow_undefined = True
    default_value = undefined
    info_text = "an instance of an object"

    def __init__(self, instance, allow_undefined=True, **kwargs):
        self.allow_undefined = allow_undefined
        super(JSONInstance, self).__init__(instance, **kwargs)

    def validate(self, obj, value):
        if self.allow_undefined and value is undefined:
            return value
        return super(JSONInstance, self).validate(obj, value)

    def make_dynamic_default(self):
        if self.allow_undefined and self.default_value is undefined:
            return undefined
        else:
            return super(JSONInstance, self).make_dynamic_default()


class JSONAnyOf(T.Union):
    """A trait whose value matches any of a list of traits"""
    allow_undefined = True
    default_value = undefined

    def __init__(self, trait_types, allow_undefined=True, **kwargs):
        self.allow_undefined = allow_undefined
        super(JSONAnyOf, self).__init__(trait_types, **kwargs)
        self.info_text = "AnyOf({0})".format(", ".join(
            tt.info() for tt in self.trait_types))

    def validate(self, obj, value):
        if self.allow_undefined and value is undefined:
            return value
        return super(JSONAnyOf, self).validate(obj, value)


class JSONOneOf(T.Union):
    """A trait whose value matches exactly one of a list of traits"""
    allow_undefined = True
    default_value = undefined

    def __init__(self, trait_types, allow_undefined=True, **kwargs):
        self.allow_undefined = allow_undefined
        super(JSONOneOf, self).__init__(trait_types, **kwargs)
        self.info_text = "OneOf({0})".format(", ".join(
            tt.info() for tt in self.trait_types))

    def validate(self, obj, value):
        if self.allow_undefined and value is undefined:
            return value

        # Should validate against only one of the trait types
        valid_count = 0
        with obj.cross_validation_lock:
            for trait_type in self.trait_types:
                try:
                    v = trait_type._validate(obj, value)
                except T.TraitError:
                    continue
                valid_count += 1
            if valid_count == 1:
                # In the case of an element trait, the name is None
                if self.name is not None:
                    setattr(obj, '_' + self.name + '_metadata',
                            trait_type.metadata)
                return v
        self.error(obj, value)


class JSONAllOf(T.Union):
    """A trait whose value matches all traits in a specified list"""
    allow_undefined = True
    default_value = undefined

    def __init__(self, trait_types, allow_undefined=True, **kwargs):
        self.allow_undefined = allow_undefined
        super(JSONAllOf, self).__init__(trait_types, **kwargs)
        self.info_text = "AllOf({0})".format(", ".join(
            tt.info() for tt in self.trait_types))

    def validate(self, obj, value):
        if self.allow_undefined and value is undefined:
            return value

        # should validate against all of the trait types
        with obj.cross_validation_lock:
            for trait_type in self.trait_types:
                v = trait_type._validate(obj, value)
        # In the case of an element trait, the name is None
        if self.name is not None:
            setattr(obj, '_' + self.name + '_metadata', trait_type.metadata)
        return v


class JSONNot(T.TraitType):
    """A trait whose value does not match the specified type"""
    allow_undefined = True
    default_value = undefined

    def __init__(self, not_this, allow_undefined=True, **kwargs):
        self.not_this = not_this
        self.allow_undefined = allow_undefined
        self.info_text = "Not({0})".format(self.not_this.info())
        super(JSONNot, self).__init__(**kwargs)

    def validate(self, obj, value):
        if self.allow_undefined and value is undefined:
            return value
        try:
            self.not_this.validate(obj, value)
        except T.TraitError:
            return value
        else:
            self.error(obj, value)



##########################################################################
# Visitor Pattern
#
# This implements to_dict() and from_dict() using an External Visitor Pattern
# built for the above classes.

class Visitor(object):
    """Class implementing the external visitor pattern"""
    def visit(self, obj, *args, **kwargs):
        methods = (getattr(self, 'visit_' + cls.__name__, None)
                   for cls in obj.__class__.__mro__)
        method = next((m for m in methods if m), self.generic_visit)
        return method(obj, *args, **kwargs)

    def clsvisit(self, obj, *args, **kwargs):
        methods = (getattr(self, 'clsvisit_' + cls.__name__, None)
                   for cls in obj.__mro__)
        method = next((m for m in methods if m), self.generic_clsvisit)
        return method(obj, *args, **kwargs)

    def generic_visit(self, obj, *args, **kwargs):
        raise NotImplementedError("visitor for {0}".format(obj))

    def generic_clsvisit(self, obj, *args, **kwargs):
        raise NotImplementedError("class visitor for {0}"
                                  "".format(obj.__class__))


class ToDict(Visitor):
    """Crawl object structure to output dictionary"""
    def generic_visit(self, obj, *args, **kwargs):
        return obj

    def visit_list(self, obj, *args, **kwargs):
        return [self.visit(o, *args, **kwargs) for o in obj]

    def visit_HasTraits(self, obj, *args, **kwargs):
        dct = {}
        for key in obj.trait_names():
            val = getattr(obj, key, undefined)
            if val is not undefined:
                dct[key] = self.visit(val, *args, **kwargs)
        return dct

    def visit_JSONHasTraits(self, obj, *args, **kwargs):
        dct = {}
        for traitlets_key in obj.trait_names():
            schema_key = obj._trait_name_map.get(traitlets_key, traitlets_key)
            if traitlets_key in obj._skip_on_export:
                continue
            val = getattr(obj, traitlets_key, undefined)
            if val is not undefined:
                dct[schema_key] = self.visit(val, *args, **kwargs)
            elif traitlets_key in obj._required_traits:
                raise UndefinedTraitError("Required trait '{0}' is undefined "
                                          "in {1}".format(traitlets_key, obj))
        for schema_key, val in obj._metadata.items():
            if val is not undefined and schema_key not in dct:
                dct[schema_key] = val
        return dct


class FromDict(Visitor):
    """Crawl object structure to construct object from a Dictionary"""
    def generic_visit(self, trait, dct, *args, **kwargs):
        if dct is None or dct is undefined:
            return dct
        if isinstance(dct, (six.integer_types, six.string_types, bool, float)):
            return dct
        else:
            raise T.TraitError('cannot set {0} to {1}'.format(trait, dct))

    def clsvisit_Any(self, cls, dct, *args, **kwargs):
        return dct

    def clsvisit_HasTraits(self, cls, dct, *args, **kwargs):
        try:
            obj = cls()
        except TypeError:  # Argument missing
            obj = cls('')

        for prop, val in dct.items():
            subtrait = obj.traits()[prop]
            obj.set_trait(prop, self.visit(subtrait, val, *args, **kwargs))
        return obj

    def clsvisit_JSONHasTraits(self, cls, dct, *args, **kwargs):
        try:
            obj = cls()
        except TypeError:  # Argument missing
            obj = cls('')
        additional_traits = cls._get_additional_traits()

        # Extract all other items, assigning to appropriate trait
        reverse_name_map = {v:k for k, v in obj._trait_name_map.items()}
        for schema_key, val in dct.items():
            if schema_key in obj._metadata:
                obj._metadata[schema_key] = val
            else:
                trait_key = reverse_name_map.get(schema_key, schema_key)
                subtrait = obj.traits().get(trait_key, additional_traits)
                if not subtrait:
                    raise T.TraitError("trait {0} not valid in class {1}"
                                       "".format(trait_key, cls))
                obj.set_trait(trait_key,
                              self.visit(subtrait, val, *args, **kwargs))

        return obj

    def visit_Instance(self, trait, dct, *args, **kwargs):
        try:
            return self.generic_visit(trait, dct)
        except T.TraitError:
            return self.clsvisit(trait.klass, dct)

    def visit_List(self, trait, dct, *args, **kwargs):
        return [self.visit(trait._trait, item, *args, **kwargs)
                for item in dct]

    def visit_Union(self, trait, dct, *args, **kwargs):
        try:
            return self.generic_visit(trait, dct)
        except T.TraitError:
            for subtrait in trait.trait_types:
                try:
                    return self.visit(subtrait, dct)
                except T.TraitError:
                    pass
            raise  # no valid trait found

    def visit_JSONNot(self, trait, dct, *args, **kwargs):
        return dct

    def clsvisit_AnyOfObject(self, trait, dct, *args, **kwargs):
        # TODO: match additional_traits as well?
        for subcls in trait._class_defs():
            if all(key in subcls.class_traits() for key in dct):
                try:
                    obj = self.clsvisit(subcls, dct)
                except (T.TraitError, ValueError):
                    pass
                else:
                    return trait(**{name: getattr(obj, name)
                                    for name in obj.trait_names()})
        else:
            raise T.TraitError("{cls}: dict representation not "
                               "valid in any wrapped classes"
                               "".format(cls=trait.__name__))


class ToPython(Visitor):
    """Crawl object structure to output Python code"""
    def generic_visit(self, obj, *args, **kwargs):
        return repr(obj)

    def visit_list(self, obj, *args, **kwargs):
        # TODO: make more compact for simple args?
        arglist = ',\n'.join(self.visit(item) for item in obj)
        return "[\n{0}\n]".format(textwrap.indent(arglist, 4 * ' '))

    def visit_JSONHasTraits(self, obj, *args, **kwargs):
        # TODO: make more compact for simple args?
        kwds = {k: getattr(obj, k) for k in obj.traits()
                if k not in obj._skip_on_export and
                getattr(obj, k, undefined) is not undefined}
        kwds = {k: self.visit(v) for k, v in kwds.items()}

        missing = set(obj._required_traits) - set(kwds)
        if missing:
            raise UndefinedTraitError("Required traits {0} missing "
                                      "in {1}".format(missing, obj))
        arglist = '\n'.join('{0}={1},'.format(*item)
                            for item in sorted(kwds.items())).rstrip(',')
        return "{0}(\n{1}\n)".format(obj.__class__.__name__,
                                     textwrap.indent(arglist, 4 * " "))
