from hgijson import MappingJSONEncoderClassBuilder, JsonPropertyMapping, MappingJSONDecoderClassBuilder, \
    DatetimeISOFormatJSONEncoder, DatetimeISOFormatJSONDecoder

from consullock.model import ConsulLockInformation


mapping_schema = [
    JsonPropertyMapping("session", "session_id", "session_id"),
    JsonPropertyMapping("created", "created", "created",
        encoder_cls=DatetimeISOFormatJSONEncoder, decoder_cls=DatetimeISOFormatJSONDecoder)
]
ConsulLockInformationJSONEncoder = MappingJSONEncoderClassBuilder(ConsulLockInformation, mapping_schema).build()
ConsulLockInformationJSONDecoder = MappingJSONDecoderClassBuilder(ConsulLockInformation, mapping_schema).build()
