# 📖 Лекция 21: Trie (Префиксное дерево)

## Что это и зачем

Trie — дерево, где каждый узел — символ. Путь от корня до узла = слово или префикс. Позволяет искать слова и префиксы за O(m), где m — длина слова.

## Когда использовать

- Автодополнение
- Проверка префиксов
- Поиск слов в словаре
- Подсчёт слов с префиксом

## Реализация

```python
class TrieNode:
    def __init__(self):
        self.children = {}
        self.is_end = False

class Trie:
    def __init__(self):
        self.root = TrieNode()
    
    def insert(self, word):
        node = self.root
        for char in word:
            if char not in node.children:
                node.children[char] = TrieNode()
            node = node.children[char]
        node.is_end = True
    
    def search(self, word):
        node = self.root
        for char in word:
            if char not in node.children:
                return False
            node = node.children[char]
        return node.is_end
    
    def starts_with(self, prefix):
        node = self.root
        for char in prefix:
            if char not in node.children:
                return False
            node = node.children[char]
        return True
```

## Word Search II

```python
def find_words(board, words):
    trie = Trie()
    for word in words:
        trie.insert(word)
    
    result = set()
    def dfs(i, j, node, path):
        char = board[i][j]
        if char not in node.children:
            return
        node = node.children[char]
        path += char
        if node.is_end:
            result.add(path)
        
        temp = board[i][j]
        board[i][j] = '#'
        for di, dj in [(0,1),(0,-1),(1,0),(-1,0)]:
            ni, nj = i + di, j + dj
            if 0 <= ni < len(board) and 0 <= nj < len(board[0]) and board[ni][nj] != '#':
                dfs(ni, nj, node, path)
        board[i][j] = temp
    
    for i in range(len(board)):
        for j in range(len(board[0])):
            dfs(i, j, trie.root, "")
    return list(result)
```

## Autocomplete System

```python
class AutocompleteSystem:
    def __init__(self, sentences, times):
        self.trie = Trie()
        self.count = {}
        for s, t in zip(sentences, times):
            self.insert(s, t)
    
    def insert(self, sentence, time):
        node = self.trie.root
        for char in sentence:
            if char not in node.children:
                node.children[char] = TrieNode()
            node = node.children[char]
        node.is_end = True
        self.count[sentence] = self.count.get(sentence, 0) + time
    
    def input(self, char):
        # Упрощённая версия
        pass
```

## Задачи на LeetCode

- Implement Trie (#208)
- Word Search II (#212)
- Design Add and Search Words Data Structure (#211)
- Replace Words (#648)
- Implement Magic Dictionary (#676)

## Где используется в Яндексе

- **Автодополнение** — поиск, адресная строка
- **Spell checker** — проверка слов
- **IP routing** — префиксные таблицы
- **URL Shortener** — быстрый lookup

## Подводные камни

- Не проверил `is_end` — префикс ≠ слово
- Забыл `children` инициализировать
- Не удалил временную метку в DFS