from modeltranslation.translator import register, TranslationOptions

from .models import (
    Service,
    Feature,
    Branch,
    MeetingRoom,
    Event,
    GalleryImage,
    FAQ,
    Contact,
)


@register(Service)
class ServiceTranslationOptions(TranslationOptions):
    fields = ("title", "description")


@register(Feature)
class FeatureTranslationOptions(TranslationOptions):
    fields = ("title", "description")


@register(Branch)
class BranchTranslationOptions(TranslationOptions):
    fields = ("name", "address", "opening_hours")


@register(MeetingRoom)
class MeetingRoomTranslationOptions(TranslationOptions):
    fields = ("name",)


@register(Event)
class EventTranslationOptions(TranslationOptions):
    fields = ("title", "description", "location")


@register(GalleryImage)
class GalleryImageTranslationOptions(TranslationOptions):
    fields = ("title",)


@register(FAQ)
class FAQTranslationOptions(TranslationOptions):
    fields = ("question", "answer")


@register(Contact)
class ContactTranslationOptions(TranslationOptions):
    fields = ()