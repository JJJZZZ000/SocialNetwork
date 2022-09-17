# from django.core.serializers import json
import json

from django.shortcuts import render
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render


class invalidWord(Exception):
    def __init__(self, msg):
        self.msg = msg

    def __str__(self):
        return self.msg


def _check(word):
    if len(word) != 5:
        raise invalidWord("Invalid input: Word length error")
    for ch in word:
        if (ch < 'a' or ch > 'z') and (ch < 'A' or ch > 'Z'):
            raise invalidWord("Invalid input: Word contains non-letter")
    return


def _checkHistory(word):
    try:
        _check(word)
    except:
        raise invalidWord("Error invalid: Hack happened, restart the game")


def _process_param(post, name):
    try:
        return post[name]
    except:
        return invalidWord("Error invalid: target changed")


def initMatrix():
    matrix = [[{} for _ in range(5)] for _ in range(6)]
    for row in range(6):
        for col in range(5):
            matrix[row][col] = {"id": "cell_" + str(row) + "_" + str(col), "letter": "",
                                "color": "background-color: white"}
    return matrix


def home(request):
    context = {}
    if request.method == 'GET':
        context["msg"] = "Welcome to wordish"
        return render(request, 'home.html', context)
    try:
        target = _process_param(request.POST, "target_text")
        _check(target)
        history = []
        matrix = initMatrix()
        context["msg"] = "Game Start"
        context["target"] = target
        context["history"] = history
        context["matrix"] = matrix
        return render(request, 'guess.html', context)
    except Exception as e:
        context = {"msg": str(e)}
        return render(request, 'home.html', context)

def deserialize(request):
    try:
        history = _process_param(request.POST, "history")
        history = history.replace("\'", "\"")
        history_ls = json.loads(history)
        return history_ls
    except:
        raise invalidWord("Error: deserialize")

def guess(request):
    context = {}
    if request.method == 'GET':
        context["msg"] = "Welcome to wordish"
        return render(request, 'home.html', context)
    try:
        ## check history data
        target = _process_param(request.POST, "target")
        _checkHistory(target)
        history_ls = deserialize(request)
        for old_guess in history_ls:
            _checkHistory(old_guess)

        matrix = initMatrix()
        ## construct the matrix below
        target_dic = {}
        for i in range(5):
            ch = target[i]
            if not target_dic.__contains__(ch):
                target_dic[ch] = 0
            target_dic[ch] = target_dic[ch] + 1

        for i in range(len(history_ls)):
            old_guess = history_ls[i]
            colors = getColor(target, old_guess, target_dic)
            # "background-color: white"
            for j in range(len(matrix[i])):
                color = colors[j]
                matrix[i][j]["letter"] = old_guess[j]
                matrix[i][j]["color"] = "background-color: " + color

        context = {
            "msg": "Game begins",
            "matrix": matrix,
            "target": target,
            "history": history_ls
        }

        ## check new guess
        word = _process_param(request.POST, "guess")
        _check(word)
        colors = getColor(target, word, target_dic)
        idx = len(history_ls)
        history_ls.append(word)
        for i in range(5):
            cell = matrix[idx][i]
            cell["letter"] = word[i]
            cell["color"] = "background-color: " + colors[i]
        if word == target:
            context["msg"] = "You Win"
        if idx == 5:
            context["msg"] = "You Lose"
        return render(request, 'guess.html', context)

    except Exception as e:
        msg = str(e)
        context["msg"] = msg
        if "Invalid input:" in msg:
            return render(request, 'guess.html', context)
        return render(request, 'home.html', context)


def getColor(target, guess, target_dic):
    colors = ["lightgray", "lightgray", "lightgray", "lightgray", "lightgray"]
    guess_dic = {}
    n = 5
    for i in range(5):
        if target[i] == guess[i]:
            colors[i] = "green"
            ch = target[i]
            if not guess_dic.__contains__(ch):
                guess_dic[ch] = 0
            guess_dic[ch] = guess_dic[ch] + 1

    for i in range(5):
        if colors[i] == "green":
            continue
        ch = guess[i]
        if target_dic.__contains__(ch):
            if not guess_dic.__contains__(ch):
                guess_dic[ch] = 0
            if guess_dic[ch] < target_dic[ch]:
                colors[i] = "yellow"
            guess_dic[ch] = guess_dic[ch] + 1
    return colors


