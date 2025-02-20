###Replay

python -m clients.main recognize file --audio-file .\Replay\1297.wav --config config.ini --enable-antispoofing --enable-punctuator 

python -m clients.main recognize file --audio-file .\Replay\1297_replay.wav --config config.ini --enable-antispoofing

python -m clients.main recognize file --audio-file .\Replay\1419.wav --config config.ini --enable-antispoofing

python -m clients.main recognize file --audio-file .\Replay\1419_replay.wav --config config.ini --enable-antispoofing



##Say-as

ssml_text = "<speak>Почему <emphasis strength='strong'>они</emphasis> не согласны?</speak>"

ssml_text = "<speak><say-as interpret-as='cardinal' format='feminine_nominative'>1</say-as> ложка</speak>"
"1 ложка"

ssml_text = "<speak>Благодарю за ожидание! Ваш баланс: 6758.9 руб. Сумма абонентской платы 1142 руб. Следующее списание произойдёт 21.12. Теперь задайте ваш вопрос.</speak>"

ssml_text = "<speak>Благодарю за ожидание! Ваш баланс: 6758.9 руб. Сумма абонентской платы 1142 руб. Следующее списание произойдёт <say-as interpret-as='date' format='genitive' detail='d.m'>21.12</say-as>. Теперь задайте ваш вопрос.</speak>"


















python -m clients.main synthesize file --text "Привет, как дела?" --config config.ini --voice-name borisova --save-to output.wav --sample-rate 44100 --model-type high_quality --voice-style neutral




