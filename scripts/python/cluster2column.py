import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.cluster import KMeans
import matplotlib.pyplot as plt

# Загрузка данных
csv_file_path = r'D:\GIT\Skills-Map\scripts\python\otf.csv'  # Замените на путь к вашему CSV файлу
data = pd.read_csv(csv_file_path)

# Группировка DTF по OTF и создание совмещенных векторов
data['combined'] = data.apply(lambda x: f"{x['NameOTF']} {x['NameDTF']}", axis=1)

# Векторизация совмещенных векторов
tfidf_vectorizer = TfidfVectorizer()
tfidf_matrix = tfidf_vectorizer.fit_transform(data['combined'])

# Определение диапазона количества кластеров для метода "локтя"
range_of_clusters = range(1, 15)

# Вычисление WCSS для каждого количества кластеров
wcss = []
for n_clusters in range_of_clusters:
    kmeans = KMeans(n_clusters=n_clusters, random_state=42)
    kmeans.fit(tfidf_matrix)
    wcss.append(kmeans.inertia_)

# Построение графика метода "локтя"
plt.figure(figsize=(10, 5))
plt.plot(range_of_clusters, wcss, marker='o', linestyle='-', color='b')
plt.title('Метод "локтя" для определения оптимального количества кластеров')
plt.xlabel('Количество кластеров')
plt.ylabel('WCSS')
plt.show()

# После визуального анализа графика, укажите оптимальное количество кластеров
optimal_clusters_otf = int(input("Введите оптимальное количество кластеров для OTF: "))
optimal_clusters_dtf = int(input("Введите оптимальное количество кластеров для DTF: "))

# Кластеризация OTF и DTF с выбранным количеством кластеров
kmeans_otf = KMeans(n_clusters=optimal_clusters_otf, random_state=42)
data['OTF_Cluster'] = kmeans_otf.fit_predict(tfidf_vectorizer.transform(data['NameOTF']))

kmeans_dtf = KMeans(n_clusters=optimal_clusters_dtf, random_state=42)
data['DTF_Cluster'] = kmeans_dtf.fit_predict(tfidf_vectorizer.transform(data['NameDTF']))

# Сохранение результатов
output_csv_file_path = 'D:\GIT\Skills-Map\scripts\python\otf-2.csv'  # Замените на путь для сохранения результата
data.to_csv(output_csv_file_path, index=False)

print(f"Результаты кластеризации сохранены в {output_csv_file_path}")
