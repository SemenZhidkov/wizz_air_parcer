#!/bin/bash
# Скрипт быстрой проверки перед деплоем

echo "🔍 Проверка проекта перед деплоем..."
echo ""

# Проверка обязательных файлов
echo "📁 Проверка файлов:"
files=(".env" "Dockerfile" "docker-compose.yml" "requirements.txt" "src/main.py" "src/parser.py" "src/bot.py")
for file in "${files[@]}"; do
    if [ -f "$file" ]; then
        echo "  ✅ $file"
    else
        echo "  ❌ $file - ОТСУТСТВУЕТ!"
        exit 1
    fi
done
echo ""

# Проверка .env
echo "🔐 Проверка .env:"
if grep -q "your_token_here" .env || grep -q "your_chat_id" .env; then
    echo "  ⚠️  ВНИМАНИЕ: .env содержит placeholder значения!"
    echo "  Не забудьте заполнить реальные значения!"
else
    echo "  ✅ .env настроен"
fi
echo ""

# Проверка структуры директорий
echo "📂 Проверка директорий:"
if [ -d "data/screenshots" ]; then
    echo "  ✅ data/screenshots"
else
    echo "  ⚠️  Создаём data/screenshots"
    mkdir -p data/screenshots
fi
echo ""

# Проверка requirements.txt
echo "📦 Проверка зависимостей:"
required_packages=("aiogram" "selenium" "undetected-chromedriver" "apscheduler")
for package in "${required_packages[@]}"; do
    if grep -q "$package" requirements.txt; then
        echo "  ✅ $package"
    else
        echo "  ❌ $package - ОТСУТСТВУЕТ!"
    fi
done
echo ""

# Git статус (если есть)
if [ -d ".git" ]; then
    echo "📝 Git статус:"
    uncommitted=$(git status --porcelain | wc -l)
    if [ $uncommitted -eq 0 ]; then
        echo "  ✅ Нет незакоммиченных изменений"
    else
        echo "  ⚠️  Есть $uncommitted незакоммиченных изменений"
        echo "  Рекомендуется сделать commit перед деплоем"
    fi
    echo ""
fi

echo "✅ Проверка завершена!"
echo ""
echo "📋 Следующие шаги:"
echo "  1. Закоммитьте изменения: git add . && git commit -m 'Ready for deploy'"
echo "  2. Запушьте в GitHub: git push"
echo "  3. На целевой машине клонируйте репозиторий"
echo "  4. Скопируйте .env с реальными значениями"
echo "  5. Запустите: docker-compose up -d"
echo ""
echo "📖 Подробнее в DEPLOY.md"
