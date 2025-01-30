"""Generated protocol buffer code."""
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import symbol_database as _symbol_database
from google.protobuf.internal import builder as _builder
_sym_db = _symbol_database.Default()
from google.protobuf import empty_pb2 as google_dot_protobuf_dot_empty__pb2
DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n\tstt.proto\x12\x17mts.ai.audiogram.stt.v3\x1a\x1bgoogle/protobuf/empty.proto"a\n\x14FileRecognizeRequest\x12:\n\x06config\x18\x01 \x01(\x0b2*.mts.ai.audiogram.stt.v3.RecognitionConfig\x12\r\n\x05audio\x18\x02 \x01(\x0c"|\n\x10RecognizeRequest\x12B\n\x06config\x18\x01 \x01(\x0b20.mts.ai.audiogram.stt.v3.StreamRecognitionConfigH\x00\x12\x0f\n\x05audio\x18\x02 \x01(\x0cH\x00B\x13\n\x11streaming_request"\xa9\x07\n\x11RecognitionConfig\x128\n\x08encoding\x18\x01 \x01(\x0e2&.mts.ai.audiogram.stt.v3.AudioEncoding\x12\x19\n\x11sample_rate_hertz\x18\x02 \x01(\r\x12\x15\n\rlanguage_code\x18\x03 \x01(\t\x12\x1b\n\x13audio_channel_count\x18\x04 \x01(\r\x12\x18\n\x10split_by_channel\x18\x05 \x01(\x08\x12\r\n\x05model\x18\x06 \x01(\t\x12 \n\x18enable_word_time_offsets\x18\x07 \x01(\x08\x12?\n\tva_config\x18\x08 \x01(\x0b2,.mts.ai.audiogram.stt.v3.VoiceActivityConfig\x12`\n\x10va_response_mode\x18\t \x01(\x0e2F.mts.ai.audiogram.stt.v3.RecognitionConfig.VoiceActivityMarkEventsMode\x12I\n\x10genderage_config\x18\n \x01(\x0b2/.mts.ai.audiogram.stt.v3.GenderAgeEmotionConfig\x12H\n\x13antispoofing_config\x18\x0b \x01(\x0b2+.mts.ai.audiogram.stt.v3.AntiSpoofingConfig\x12L\n\x12context_dictionary\x18\x0c \x01(\x0b20.mts.ai.audiogram.stt.v3.ContextDictionaryConfig\x12F\n\x12punctuation_config\x18\r \x01(\x0b2*.mts.ai.audiogram.stt.v3.PunctuationConfig\x12N\n\x16denormalization_config\x18\x0e \x01(\x0b2..mts.ai.audiogram.stt.v3.DenormalizationConfig\x12O\n\x17speaker_labeling_config\x18\x0f \x01(\x0b2..mts.ai.audiogram.stt.v3.SpeakerLabelingConfig"Q\n\x1bVoiceActivityMarkEventsMode\x12\x0e\n\nVA_DISABLE\x10\x00\x12\r\n\tVA_ENABLE\x10\x01\x12\x13\n\x0fVA_ENABLE_ASYNC\x10\x02"\x88\x01\n\x17StreamRecognitionConfig\x12:\n\x06config\x18\x01 \x01(\x0b2*.mts.ai.audiogram.stt.v3.RecognitionConfig\x12\x18\n\x10single_utterance\x18\x02 \x01(\x08\x12\x17\n\x0finterim_results\x18\x03 \x01(\x08"\xe4\x02\n\x13VoiceActivityConfig\x12`\n\x05usage\x18\x01 \x01(\x0e2Q.mts.ai.audiogram.stt.v3.VoiceActivityConfig.VoiceActivityDetectionAlgorithmUsage\x12:\n\x0bvad_options\x18\x02 \x01(\x0b2#.mts.ai.audiogram.stt.v3.VADOptionsH\x00\x12:\n\x0bdep_options\x18\x03 \x01(\x0b2#.mts.ai.audiogram.stt.v3.DEPOptionsH\x00"c\n$VoiceActivityDetectionAlgorithmUsage\x12\x0b\n\x07USE_VAD\x10\x00\x12!\n\x1dDO_NOT_PERFORM_VOICE_ACTIVITY\x10\x01\x12\x0b\n\x07USE_DEP\x10\x02B\x0e\n\x0calgo_options"\x8d\x02\n\nVADOptions\x12\x11\n\tthreshold\x18\x01 \x01(\x02\x12\x15\n\rspeech_pad_ms\x18\x02 \x01(\x05\x12\x16\n\x0emin_silence_ms\x18\x03 \x01(\r\x12\x15\n\rmin_speech_ms\x18\x04 \x01(\r\x12L\n\x04mode\x18\x05 \x01(\x0e2>.mts.ai.audiogram.stt.v3.VADOptions.VoiceActivityDetectionMode"X\n\x1aVoiceActivityDetectionMode\x12\x14\n\x10VAD_MODE_DEFAULT\x10\x00\x12\x13\n\x0fSPLIT_BY_PAUSES\x10\x01\x12\x0f\n\x0bONLY_SPEECH\x10\x02"K\n\nDEPOptions\x12!\n\x19smoothed_window_threshold\x18\x01 \x01(\x02\x12\x1a\n\x12smoothed_window_ms\x18\x02 \x01(\x05"(\n\x16GenderAgeEmotionConfig\x12\x0e\n\x06enable\x18\x01 \x01(\x08"\xae\x01\n\x12AntiSpoofingConfig\x121\n\x04type\x18\x01 \x01(\x0e2#.mts.ai.audiogram.stt.v3.AttackType\x12\r\n\x03FAR\x18\x02 \x01(\x02H\x00\x12\r\n\x03FRR\x18\x03 \x01(\x02H\x00\x12$\n\x1cmax_duration_for_analysis_ms\x18\x04 \x01(\r\x12\x0e\n\x06enable\x18\x05 \x01(\x08B\x11\n\x0ffalse_rate_type"B\n\x17ContextDictionaryConfig\x12\x17\n\x0fdictionary_name\x18\x01 \x01(\t\x12\x0e\n\x06weight\x18\x02 \x01(\x02"#\n\x11PunctuationConfig\x12\x0e\n\x06enable\x18\x01 \x01(\x08"\'\n\x15DenormalizationConfig\x12\x0e\n\x06enable\x18\x01 \x01(\x08"c\n\x15SpeakerLabelingConfig\x12\x0e\n\x06enable\x18\x01 \x01(\x08\x12\x16\n\x0cmax_speakers\x18\x02 \x01(\rH\x00\x12\x16\n\x0cnum_speakers\x18\x03 \x01(\rH\x00B\n\n\x08speakers"U\n\x15FileRecognizeResponse\x12<\n\x08response\x18\x01 \x03(\x0b2*.mts.ai.audiogram.stt.v3.RecognizeResponse"\x84\x03\n\x11RecognizeResponse\x12H\n\nhypothesis\x18\x01 \x01(\x0b24.mts.ai.audiogram.stt.v3.SpeechRecognitionHypothesis\x12\x10\n\x08is_final\x18\x02 \x01(\x08\x12\x0f\n\x07channel\x18\x03 \x01(\x05\x12<\n\x08va_marks\x18\x04 \x03(\x0b2*.mts.ai.audiogram.stt.v3.VoiceActivityMark\x12F\n\tgenderage\x18\x05 \x01(\x0b23.mts.ai.audiogram.stt.v3.SpeakerGenderAgePrediction\x12@\n\x0fspoofing_result\x18\x06 \x03(\x0b2\'.mts.ai.audiogram.stt.v3.SpoofingResult\x12:\n\x0cspeaker_info\x18\x07 \x01(\x0b2$.mts.ai.audiogram.stt.v3.SpeakerInfo"\x91\x03\n\x1bSpeechRecognitionHypothesis\x12\x12\n\ntranscript\x18\x01 \x01(\t\x12\x1d\n\x15normalized_transcript\x18\x02 \x01(\t\x12\x12\n\nconfidence\x18\x03 \x01(\x02\x12\x15\n\rstart_time_ms\x18\x04 \x01(\r\x12\x13\n\x0bend_time_ms\x18\x05 \x01(\r\x12L\n\x05words\x18\x06 \x03(\x0b2=.mts.ai.audiogram.stt.v3.SpeechRecognitionHypothesis.WordInfo\x12W\n\x10normalized_words\x18\x07 \x03(\x0b2=.mts.ai.audiogram.stt.v3.SpeechRecognitionHypothesis.WordInfo\x1aX\n\x08WordInfo\x12\x15\n\rstart_time_ms\x18\x01 \x01(\r\x12\x13\n\x0bend_time_ms\x18\x02 \x01(\r\x12\x0c\n\x04word\x18\x03 \x01(\t\x12\x12\n\nconfidence\x18\x04 \x01(\x02"\xca\x01\n\x11VoiceActivityMark\x12S\n\tmark_type\x18\x01 \x01(\x0e2@.mts.ai.audiogram.stt.v3.VoiceActivityMark.VoiceActivityMarkType\x12\x11\n\toffset_ms\x18\x02 \x01(\r"M\n\x15VoiceActivityMarkType\x12\x10\n\x0cVA_MARK_NONE\x10\x00\x12\x11\n\rVA_MARK_BEGIN\x10\x01\x12\x0f\n\x0bVA_MARK_END\x10\x02"\xf8\x03\n\x1aSpeakerGenderAgePrediction\x12O\n\x06gender\x18\x01 \x01(\x0e2?.mts.ai.audiogram.stt.v3.SpeakerGenderAgePrediction.GenderClass\x12I\n\x03age\x18\x02 \x01(\x0e2<.mts.ai.audiogram.stt.v3.SpeakerGenderAgePrediction.AgeClass\x12X\n\x07emotion\x18\x03 \x01(\x0b2G.mts.ai.audiogram.stt.v3.SpeakerGenderAgePrediction.EmotionsRecognition\x1af\n\x13EmotionsRecognition\x12\x10\n\x08positive\x18\x01 \x01(\x02\x12\x0f\n\x07neutral\x18\x02 \x01(\x02\x12\x16\n\x0enegative_angry\x18\x03 \x01(\x02\x12\x14\n\x0cnegative_sad\x18\x04 \x01(\x02"C\n\x0bGenderClass\x12\x10\n\x0cGENDER_UNDEF\x10\x00\x12\x0f\n\x0bGENDER_MALE\x10\x01\x12\x11\n\rGENDER_FEMALE\x10\x02"7\n\x08AgeClass\x12\r\n\tAGE_UNDEF\x10\x00\x12\r\n\tAGE_ADULT\x10\x01\x12\r\n\tAGE_CHILD\x10\x02"\xfb\x01\n\x0eSpoofingResult\x121\n\x04type\x18\x01 \x01(\x0e2#.mts.ai.audiogram.stt.v3.AttackType\x12D\n\x06result\x18\x02 \x01(\x0e24.mts.ai.audiogram.stt.v3.SpoofingResult.AttackResult\x12\x12\n\nconfidence\x18\x03 \x01(\x02\x12\x15\n\rstart_time_ms\x18\x04 \x01(\r\x12\x13\n\x0bend_time_ms\x18\x05 \x01(\r"0\n\x0cAttackResult\x12\x13\n\x0fATTACK_DETECTED\x10\x00\x12\x0b\n\x07GENUINE\x10\x01"!\n\x0bSpeakerInfo\x12\x12\n\nspeaker_id\x18\x01 \x01(\r"@\n\nModelsInfo\x122\n\x06models\x18\x01 \x03(\x0b2".mts.ai.audiogram.stt.v3.ModelInfo"d\n\tModelInfo\x12\x0c\n\x04name\x18\x01 \x01(\t\x12\x19\n\x11sample_rate_hertz\x18\x02 \x01(\r\x12\x15\n\rlanguage_code\x18\x03 \x01(\t\x12\x17\n\x0fdictionary_name\x18\x04 \x03(\t*X\n\rAudioEncoding\x12\x18\n\x14ENCODING_UNSPECIFIED\x10\x00\x12\x0e\n\nLINEAR_PCM\x10\x01\x12\x08\n\x04FLAC\x10\x02\x12\t\n\x05MULAW\x10\x03\x12\x08\n\x04ALAW\x10\x14*6\n\nAttackType\x12\x0b\n\x07LOGICAL\x10\x00\x12\x0c\n\x08PHYSICAL\x10\x01\x12\r\n\tALL_TYPES\x10\x022\xab\x02\n\x03STT\x12n\n\rFileRecognize\x12-.mts.ai.audiogram.stt.v3.FileRecognizeRequest\x1a..mts.ai.audiogram.stt.v3.FileRecognizeResponse\x12f\n\tRecognize\x12).mts.ai.audiogram.stt.v3.RecognizeRequest\x1a*.mts.ai.audiogram.stt.v3.RecognizeResponse(\x010\x01\x12L\n\rGetModelsInfo\x12\x16.google.protobuf.Empty\x1a#.mts.ai.audiogram.stt.v3.ModelsInfob\x06proto3')
_globals = globals()
_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, _globals)
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'stt_pb2', _globals)
if _descriptor._USE_C_DESCRIPTORS == False:
    DESCRIPTOR._options = None
    _globals['_AUDIOENCODING']._serialized_start = 4596
    _globals['_AUDIOENCODING']._serialized_end = 4684
    _globals['_ATTACKTYPE']._serialized_start = 4686
    _globals['_ATTACKTYPE']._serialized_end = 4740
    _globals['_FILERECOGNIZEREQUEST']._serialized_start = 67
    _globals['_FILERECOGNIZEREQUEST']._serialized_end = 164
    _globals['_RECOGNIZEREQUEST']._serialized_start = 166
    _globals['_RECOGNIZEREQUEST']._serialized_end = 290
    _globals['_RECOGNITIONCONFIG']._serialized_start = 293
    _globals['_RECOGNITIONCONFIG']._serialized_end = 1230
    _globals['_RECOGNITIONCONFIG_VOICEACTIVITYMARKEVENTSMODE']._serialized_start = 1149
    _globals['_RECOGNITIONCONFIG_VOICEACTIVITYMARKEVENTSMODE']._serialized_end = 1230
    _globals['_STREAMRECOGNITIONCONFIG']._serialized_start = 1233
    _globals['_STREAMRECOGNITIONCONFIG']._serialized_end = 1369
    _globals['_VOICEACTIVITYCONFIG']._serialized_start = 1372
    _globals['_VOICEACTIVITYCONFIG']._serialized_end = 1728
    _globals['_VOICEACTIVITYCONFIG_VOICEACTIVITYDETECTIONALGORITHMUSAGE']._serialized_start = 1613
    _globals['_VOICEACTIVITYCONFIG_VOICEACTIVITYDETECTIONALGORITHMUSAGE']._serialized_end = 1712
    _globals['_VADOPTIONS']._serialized_start = 1731
    _globals['_VADOPTIONS']._serialized_end = 2000
    _globals['_VADOPTIONS_VOICEACTIVITYDETECTIONMODE']._serialized_start = 1912
    _globals['_VADOPTIONS_VOICEACTIVITYDETECTIONMODE']._serialized_end = 2000
    _globals['_DEPOPTIONS']._serialized_start = 2002
    _globals['_DEPOPTIONS']._serialized_end = 2077
    _globals['_GENDERAGEEMOTIONCONFIG']._serialized_start = 2079
    _globals['_GENDERAGEEMOTIONCONFIG']._serialized_end = 2119
    _globals['_ANTISPOOFINGCONFIG']._serialized_start = 2122
    _globals['_ANTISPOOFINGCONFIG']._serialized_end = 2296
    _globals['_CONTEXTDICTIONARYCONFIG']._serialized_start = 2298
    _globals['_CONTEXTDICTIONARYCONFIG']._serialized_end = 2364
    _globals['_PUNCTUATIONCONFIG']._serialized_start = 2366
    _globals['_PUNCTUATIONCONFIG']._serialized_end = 2401
    _globals['_DENORMALIZATIONCONFIG']._serialized_start = 2403
    _globals['_DENORMALIZATIONCONFIG']._serialized_end = 2442
    _globals['_SPEAKERLABELINGCONFIG']._serialized_start = 2444
    _globals['_SPEAKERLABELINGCONFIG']._serialized_end = 2543
    _globals['_FILERECOGNIZERESPONSE']._serialized_start = 2545
    _globals['_FILERECOGNIZERESPONSE']._serialized_end = 2630
    _globals['_RECOGNIZERESPONSE']._serialized_start = 2633
    _globals['_RECOGNIZERESPONSE']._serialized_end = 3021
    _globals['_SPEECHRECOGNITIONHYPOTHESIS']._serialized_start = 3024
    _globals['_SPEECHRECOGNITIONHYPOTHESIS']._serialized_end = 3425
    _globals['_SPEECHRECOGNITIONHYPOTHESIS_WORDINFO']._serialized_start = 3337
    _globals['_SPEECHRECOGNITIONHYPOTHESIS_WORDINFO']._serialized_end = 3425
    _globals['_VOICEACTIVITYMARK']._serialized_start = 3428
    _globals['_VOICEACTIVITYMARK']._serialized_end = 3630
    _globals['_VOICEACTIVITYMARK_VOICEACTIVITYMARKTYPE']._serialized_start = 3553
    _globals['_VOICEACTIVITYMARK_VOICEACTIVITYMARKTYPE']._serialized_end = 3630
    _globals['_SPEAKERGENDERAGEPREDICTION']._serialized_start = 3633
    _globals['_SPEAKERGENDERAGEPREDICTION']._serialized_end = 4137
    _globals['_SPEAKERGENDERAGEPREDICTION_EMOTIONSRECOGNITION']._serialized_start = 3909
    _globals['_SPEAKERGENDERAGEPREDICTION_EMOTIONSRECOGNITION']._serialized_end = 4011
    _globals['_SPEAKERGENDERAGEPREDICTION_GENDERCLASS']._serialized_start = 4013
    _globals['_SPEAKERGENDERAGEPREDICTION_GENDERCLASS']._serialized_end = 4080
    _globals['_SPEAKERGENDERAGEPREDICTION_AGECLASS']._serialized_start = 4082
    _globals['_SPEAKERGENDERAGEPREDICTION_AGECLASS']._serialized_end = 4137
    _globals['_SPOOFINGRESULT']._serialized_start = 4140
    _globals['_SPOOFINGRESULT']._serialized_end = 4391
    _globals['_SPOOFINGRESULT_ATTACKRESULT']._serialized_start = 4343
    _globals['_SPOOFINGRESULT_ATTACKRESULT']._serialized_end = 4391
    _globals['_SPEAKERINFO']._serialized_start = 4393
    _globals['_SPEAKERINFO']._serialized_end = 4426
    _globals['_MODELSINFO']._serialized_start = 4428
    _globals['_MODELSINFO']._serialized_end = 4492
    _globals['_MODELINFO']._serialized_start = 4494
    _globals['_MODELINFO']._serialized_end = 4594
    _globals['_STT']._serialized_start = 4743
    _globals['_STT']._serialized_end = 5042