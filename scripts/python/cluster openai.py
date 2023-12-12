import openai
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.cluster import KMeans

# Функция для генерации обобщений с помощью OpenAI API
def generate_summary(descriptions):
    """
    Использует OpenAI API для генерации обобщенного описания для списка трудовых функций.
    """
    max_tokens = 1000  # Максимальное количество токенов для одного запроса
    summaries = []

    # Если описание слишком длинное, разбиваем на части
    if len(descriptions) > max_tokens:
        for i in range(0, len(descriptions), max_tokens):
            part_descriptions = descriptions[i:i+max_tokens]
            try:
                response = openai.Completion.create(
                    engine="text-davinci-003",
                    prompt="\n".join(part_descriptions) + "\n\nОбобщение:",
                    temperature=0.7,
                    max_tokens=50,
                    top_p=1,
                    frequency_penalty=0,
                    presence_penalty=0
                )
                summary = response.choices[0].text.strip()
                summaries.append(summary)
            except openai.error.OpenAIError as e:
                print(f"An error occurred: {e}")
    else:
        try:
            response = openai.Completion.create(
                engine="text-davinci-003",
                prompt="\n".join(descriptions) + "\n\nОбобщение:",
                temperature=0.7,
                max_tokens=50,
                top_p=1,
                frequency_penalty=0,
                presence_penalty=0
            )
            summary = response.choices[0].text.strip()
            summaries.append(summary)
        except openai.error.OpenAIError as e:
            print(f"An error occurred: {e}")

    return ' '.join(summaries) if summaries else None

# Установите ваш ключ API OpenAI
openai.api_key = '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'

# Считываем данные из файла CSV
file_path = r'D:\GIT\Skills-Map\scripts\python\otf.csv'

data = pd.read_csv(file_path)

# Объединяем и нормализуем тексты OTF и DTF
combined_descriptions = pd.concat([data['NameOTF'], data['NameDTF']]).unique().tolist()

# Создаем новый DataFrame для кластеризации
combined_df = pd.DataFrame({'description': combined_descriptions})

# Преобразуем тексты в числовые вектора с помощью TF-IDF
tfidf_vectorizer = TfidfVectorizer(stop_words=None)  # Можете использовать специальный список стоп-слов для русского языка
tfidf_matrix = tfidf_vectorizer.fit_transform(combined_df['description'])

# Применяем алгоритм кластеризации K-Means
kmeans = KMeans(n_clusters=15, n_init=10, random_state=42)
kmeans.fit(tfidf_matrix)

# Присваиваем метки кластеров
combined_df['cluster'] = kmeans.labels_

# Генерируем обобщения для каждого кластера OTF и DTF
summaries = {}
for cluster_num in range(kmeans.n_clusters):
    cluster_descriptions = combined_df[combined_df['cluster'] == cluster_num]['description'].tolist()
    if cluster_descriptions:
        summary = generate_summary(cluster_descriptions)
        summaries[cluster_num] = summary
    else:
        summaries[cluster_num] = None

# Сохраняем результаты в CSV-файл
output_file_path = file_path.replace('.csv', '_summaries.csv')
with open(output_file_path, 'w', encoding='utf-8') as f:
    f.write('cluster,summary\n')
    for cluster_num, summary in summaries.items():
        f.write(f'"{cluster_num}","{summary}"\n')

print(f"Обобщения сохранены в файле: {output_file_path}")
