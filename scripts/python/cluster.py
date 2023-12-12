import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.cluster import KMeans

# Укажите путь к файлу CSV и имя столбца для считывания названий процессов
csv_file_path = r'D:\GIT\Skills-Map\scripts\python\otf.csv'
column_name = 'NameOTF'
output_csv_file_path = r'D:\GIT\Skills-Map\scripts\python\otf-2.csv'

# Загрузите данные из файла CSV
data = pd.read_csv(csv_file_path)

# Создайте список названий процессов из выбранного столбца
process_names = data[column_name].tolist()

# Определите веса для начала и конца текста
start_weight = 2.0
end_weight = 1.0

# Создайте функцию для токенизации и присвоения весов
def custom_tokenizer(text):
    tokens = text.split()
    num_tokens = len(tokens)
    weighted_tokens = []
    for i, token in enumerate(tokens):
        if i < num_tokens // 2:  # Устанавливаем вес для первой половины токенов
            weighted_tokens.append(f"{token} * {start_weight}")
        else:
            weighted_tokens.append(f"{token} * {end_weight}")
    return weighted_tokens

# Преобразуйте названия в числовой формат с использованием TF-IDF и своей функции токенизации
tfidf_vectorizer = TfidfVectorizer(tokenizer=lambda x: x, lowercase=False)
tfidf_matrix = tfidf_vectorizer.fit_transform([custom_tokenizer(process) for process in process_names])

# Определите оптимальное количество кластеров с использованием метода "локтя"
wcss = []  # Within-Cluster-Sum-of-Squares
for i in range(1, 11):
    kmeans = KMeans(n_clusters=i, init='k-means++', max_iter=300, n_init=10, random_state=0)
    kmeans.fit(tfidf_matrix)
    wcss.append(kmeans.inertia_)

# Выберите оптимальное количество кластеров (например, по "локтю")
optimal_num_clusters = 15  # Замените на оптимальное значение

# Примените алгоритм K-Means с оптимальным количеством кластеров
kmeans = KMeans(n_clusters=optimal_num_clusters)
kmeans.fit(tfidf_matrix)

# Добавьте столбец с номером кластера к исходным данным
data['Cluster'] = kmeans.labels_

# Сохраните результаты в новый CSV файл
data.to_csv(output_csv_file_path, index=False)

print(f"Результаты кластеризации сохранены в {output_csv_file_path}")
