lines = [
    "Увезу молую в Рим, увезу молую в Лондон",
    "Я хочу любить всю жизнь - и это пипец как долго",
    "Но это пипец как быстро, ведь это пипец как классно",
    "Фото на чьей-то днюхе, рандомное фото с трассы",
    "Фото на Новый Год, или фото с фоном паласа",
    "Фото на фоне Луны, или фото дома с матрасом",
    "Люблю тебя на всех фотках, люблю тебя во всех жизнях",
    "Со мной жить пипец сложно, но без тебя нет жизни",
]

with open("practice_2.1/resource/text.txt", "w", encoding="utf-8") as f:
    for line in lines:
        f.write(line + "\n")

with open("practice_2.1/resource/text.txt", "r", encoding="utf-8") as f:
    file_lines = f.readlines()

line_count = len(file_lines)
word_count = 0
vowels = 0
consonants = 0
vowel_letters = "aeiouAEIOU"
russian_vowels = "аеёиоуыэюяАЕЁИОУЫЭЮЯ"
longest_line = ""

for line in file_lines:
    stripped_line = line.rstrip("\n")

    if len(stripped_line) > len(longest_line):
        longest_line = stripped_line

    word_count += len(stripped_line.split())

    for ch in stripped_line:
        if ch.isalpha():
            if ch in vowel_letters or ch in russian_vowels:
                vowels += 1
            else:
                consonants += 1

print("Кол-во строк:", line_count)
print("Кол-во слов:", word_count)
print("Самая длинная строка:", longest_line)
print("Кол-во гласных букв:", vowels)
print("Кол-во согласных букв:", consonants)