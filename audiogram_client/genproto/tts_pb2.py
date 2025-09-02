"""Generated protocol buffer code."""
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import symbol_database as _symbol_database
from google.protobuf.internal import builder as _builder
_sym_db = _symbol_database.Default()
from google.protobuf import empty_pb2 as google_dot_protobuf_dot_empty__pb2
DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n\ttts.proto\x12\x17mts.ai.audiogram.tts.v2\x1a\x1bgoogle/protobuf/empty.proto"\xe1\x05\n\x11SynthesizeOptions\x12\x12\n\nmodel_type\x18\x02 \x01(\t\x12\x1f\n\x17model_sample_rate_hertz\x18\x03 \x01(\r\x128\n\x0bvoice_style\x18\x05 \x01(\x0e2#.mts.ai.audiogram.tts.v2.VoiceStyle\x12Z\n\x13postprocessing_mode\x18\x07 \x01(\x0e2=.mts.ai.audiogram.tts.v2.SynthesizeOptions.PostprocessingMode\x12U\n\x0ecustom_options\x18\x0b \x03(\x0b2=.mts.ai.audiogram.tts.v2.SynthesizeOptions.CustomOptionsEntry\x1a\x99\x01\n\x1bCustomSynthesizeOptionValue\x12\x15\n\x0bint32_value\x18\x01 \x01(\x05H\x00\x12\x15\n\x0bint64_value\x18\x02 \x01(\x03H\x00\x12\x16\n\x0cnumber_value\x18\x03 \x01(\x01H\x00\x12\x16\n\x0cstring_value\x18\x04 \x01(\tH\x00\x12\x14\n\nbool_value\x18\x05 \x01(\x08H\x00B\x06\n\x04kind\x1a|\n\x12CustomOptionsEntry\x12\x0b\n\x03key\x18\x01 \x01(\t\x12U\n\x05value\x18\x02 \x01(\x0b2F.mts.ai.audiogram.tts.v2.SynthesizeOptions.CustomSynthesizeOptionValue:\x028\x01"r\n\x12PostprocessingMode\x12\x1b\n\x17POST_PROCESSING_DISABLE\x10\x00\x12!\n\x1dPOST_PROCESSING_PHONE_CHANNEL\x10\x01\x12\x1c\n\x18POST_PROCESSING_PRETTIFY\x10\x02J\x04\x08\x01\x10\x02J\x04\x08\x04\x10\x05J\x04\x08\x06\x10\x07J\x04\x08\x08\x10\tJ\x04\x08\t\x10\n"\x91\x02\n\x17SynthesizeSpeechRequest\x12\x0e\n\x04text\x18\x01 \x01(\tH\x00\x12\x0e\n\x04ssml\x18\x02 \x01(\tH\x00\x12\x15\n\rlanguage_code\x18\x03 \x01(\t\x128\n\x08encoding\x18\x04 \x01(\x0e2&.mts.ai.audiogram.tts.v2.AudioEncoding\x12\x19\n\x11sample_rate_hertz\x18\x05 \x01(\x05\x12\x12\n\nvoice_name\x18\x06 \x01(\t\x12F\n\x12synthesize_options\x18\x07 \x01(\x0b2*.mts.ai.audiogram.tts.v2.SynthesizeOptionsB\x0e\n\x0cinput_source"2\n!StreamingSynthesizeSpeechResponse\x12\r\n\x05audio\x18\x01 \x01(\x0c")\n\x18SynthesizeSpeechResponse\x12\r\n\x05audio\x18\x01 \x01(\x0c"@\n\nModelsInfo\x122\n\x06models\x18\x01 \x03(\x0b2".mts.ai.audiogram.tts.v2.ModelInfo"Y\n\tModelInfo\x12\x0c\n\x04name\x18\x01 \x01(\t\x12\x19\n\x11sample_rate_hertz\x18\x02 \x01(\r\x12\x15\n\rlanguage_code\x18\x03 \x01(\t\x12\x0c\n\x04type\x18\x04 \x01(\t*X\n\rAudioEncoding\x12\x18\n\x14ENCODING_UNSPECIFIED\x10\x00\x12\x0e\n\nLINEAR_PCM\x10\x01\x12\x08\n\x04FLAC\x10\x02\x12\t\n\x05MULAW\x10\x03\x12\x08\n\x04ALAW\x10\x14*\x83\x01\n\nVoiceStyle\x12\x17\n\x13VOICE_STYLE_NEUTRAL\x10\x00\x12\x15\n\x11VOICE_STYLE_HAPPY\x10\x01\x12\x15\n\x11VOICE_STYLE_ANGRY\x10\x02\x12\x13\n\x0fVOICE_STYLE_SAD\x10\x03\x12\x19\n\x15VOICE_STYLE_SURPRISED\x10\x042\xce\x02\n\x03TTS\x12\x85\x01\n\x13StreamingSynthesize\x120.mts.ai.audiogram.tts.v2.SynthesizeSpeechRequest\x1a:.mts.ai.audiogram.tts.v2.StreamingSynthesizeSpeechResponse0\x01\x12q\n\nSynthesize\x120.mts.ai.audiogram.tts.v2.SynthesizeSpeechRequest\x1a1.mts.ai.audiogram.tts.v2.SynthesizeSpeechResponse\x12L\n\rGetModelsInfo\x12\x16.google.protobuf.Empty\x1a#.mts.ai.audiogram.tts.v2.ModelsInfob\x06proto3')
_globals = globals()
_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, _globals)
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'tts_pb2', _globals)
if _descriptor._USE_C_DESCRIPTORS == False:
    DESCRIPTOR._options = None
    _SYNTHESIZEOPTIONS_CUSTOMOPTIONSENTRY._options = None
    _SYNTHESIZEOPTIONS_CUSTOMOPTIONSENTRY._serialized_options = b'8\x01'
    _globals['_AUDIOENCODING']._serialized_start = 1335
    _globals['_AUDIOENCODING']._serialized_end = 1423
    _globals['_VOICESTYLE']._serialized_start = 1426
    _globals['_VOICESTYLE']._serialized_end = 1557
    _globals['_SYNTHESIZEOPTIONS']._serialized_start = 68
    _globals['_SYNTHESIZEOPTIONS']._serialized_end = 805
    _globals['_SYNTHESIZEOPTIONS_CUSTOMSYNTHESIZEOPTIONVALUE']._serialized_start = 380
    _globals['_SYNTHESIZEOPTIONS_CUSTOMSYNTHESIZEOPTIONVALUE']._serialized_end = 533
    _globals['_SYNTHESIZEOPTIONS_CUSTOMOPTIONSENTRY']._serialized_start = 535
    _globals['_SYNTHESIZEOPTIONS_CUSTOMOPTIONSENTRY']._serialized_end = 659
    _globals['_SYNTHESIZEOPTIONS_POSTPROCESSINGMODE']._serialized_start = 661
    _globals['_SYNTHESIZEOPTIONS_POSTPROCESSINGMODE']._serialized_end = 775
    _globals['_SYNTHESIZESPEECHREQUEST']._serialized_start = 808
    _globals['_SYNTHESIZESPEECHREQUEST']._serialized_end = 1081
    _globals['_STREAMINGSYNTHESIZESPEECHRESPONSE']._serialized_start = 1083
    _globals['_STREAMINGSYNTHESIZESPEECHRESPONSE']._serialized_end = 1133
    _globals['_SYNTHESIZESPEECHRESPONSE']._serialized_start = 1135
    _globals['_SYNTHESIZESPEECHRESPONSE']._serialized_end = 1176
    _globals['_MODELSINFO']._serialized_start = 1178
    _globals['_MODELSINFO']._serialized_end = 1242
    _globals['_MODELINFO']._serialized_start = 1244
    _globals['_MODELINFO']._serialized_end = 1333
    _globals['_TTS']._serialized_start = 1560
    _globals['_TTS']._serialized_end = 1894