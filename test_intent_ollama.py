from pita.backend.intent.parser import IntentParser

p = IntentParser()
print(p.parse("open my documents folder"))
print(p.parse("search best restaurants in lagos"))
print(p.parse("type Hello, this is a test"))
