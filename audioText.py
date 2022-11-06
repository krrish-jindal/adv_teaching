import speech_recognition as sr
import pyttsx3
import nlpcloud

r = sr.Recognizer()

def SpeakText(command):
    engine = pyttsx3.init()
    engine.say(command)
    engine.runAndWait()

mytext = ''
while (1):
    try:
        with sr.Microphone() as source2:
            r.adjust_for_ambient_noise(source2, duration=0.2)
            audio2 = r.listen(source2)
            MyText = r.recognize_google(audio2)
            MyText = MyText.lower()
            print(MyText)
            mytext = mytext + ' ' + str(MyText)
            with open("sample.html", "a") as file_object:
                file_object.write(str(MyText) + '.')
            if MyText == 'lecture finished':
                client = nlpcloud.Client("bart-large-cnn", "Your_Token")
                print("...Summarizing...")
                r = client.summarization(f"""{mytext}""")
                print(r)
                with open("sz.txt", "a") as file_object:
                    file_object.write(r['summary_text'])
                    break

    except sr.RequestError as e:
        print("Could not request results; {0}".format(e))
    except sr.UnknownValueError:
        print("unknown error occured")