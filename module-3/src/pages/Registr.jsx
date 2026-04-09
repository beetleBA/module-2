import { useEffect, useMemo, useState } from "react";
import { useNavigate } from "react-router-dom";

export const Registr = () => {
  const [recipes, setRecipes] = useState([]);
  const [sortConfig, setSortConfig] = useState({
    key: "createdAt",
    direction: "desc",
  });

  // Загрузка рецептов (замените на fetch('/api/recipes'))
  useEffect(() => {
    // const fetchRecipes = async () => {
    //   const res = await fetch('/api/recipes');
    //   setRecipes(await res.json());
    // };
    // fetchRecipes();

    // Мок для примера
    setRecipes([
      {
        id: 1,
        title: "Борщ",
        description: "Классический украинский суп",
        calories: 120,
        time: 60,
        image: "borch.jpg",
        createdAt: new Date("2026-04-08"),
      },
      {
        id: 2,
        title: "Паста Карбонара",
        description: "Итальянская паста с яйцом и сыром",
        calories: 550,
        time: 20,
        image: "pasta.jpg",
        createdAt: new Date("2026-04-09"),
      },
      {
        id: 3,
        title: "Салат Цезарь",
        description: "Курица, сухарики, соус",
        calories: 350,
        time: 15,
        image: "caesar.jpg",
        createdAt: new Date("2026-04-07"),
      },
    ]);
  }, []);

  // Сортировка
  const sortedRecipes = useMemo(() => {
    let sorted = [...recipes];
    if (sortConfig.key) {
      sorted.sort((a, b) => {
        let aVal = a[sortConfig.key];
        let bVal = b[sortConfig.key];
        if (sortConfig.key === "createdAt") {
          aVal = new Date(aVal);
          bVal = new Date(bVal);
        }
        if (aVal > bVal) {
          return sortConfig.direction === "asc" ? 1 : -1;
        }
        if (aVal < bVal) {
          return sortConfig.direction === "asc" ? -1 : 1;
        }

        return 0;
      });
    }
    return sorted;
  }, [recipes, sortConfig]);

  const requestSort = (key) => {
    let direction = "asc";
    if (sortConfig.key === key && sortConfig.direction === "asc") {
      direction = "desc";
    }
    setSortConfig({ key, direction });
  };

  const getSortIcon = (key) => {
    if (sortConfig.key !== key) return "↕️";
    return sortConfig.direction === "asc" ? "↑" : "↓";
  };

  if (recipes.length === 0) return <p>Загрузка...</p>;

  return (
    <div className="recipes-list p-4 max-w-6xl mx-auto">
      <h1 className="text-3xl font-bold mb-6">Рецепты</h1>
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
        {sortedRecipes.map((recipe) => (
          <div
            key={recipe.id}
            className="bg-white rounded-lg shadow-md overflow-hidden hover:shadow-xl transition-shadow"
          >
            <img
              src={recipe.image}
              alt={recipe.title}
              className="w-full h-48 object-cover"
            />
            <div className="p-4">
              <h2 className="text-xl font-semibold mb-2">{recipe.title}</h2>
              <p className="text-gray-600 mb-3 line-clamp-2">
                {recipe.description}
              </p>
              <div className="flex justify-between text-sm text-gray-500 mb-2">
                <span>Калории: {recipe.calories} ккал</span>
                <span>{recipe.time} мин</span>
              </div>
            </div>
          </div>
        ))}
      </div>

      {/* Таблица сортировки (опционально под списком) */}
      <div className="mt-8 overflow-x-auto">
        <table className="min-w-full bg-white border">
          <thead>
            <tr>
              <th
                className="px-4 py-2 cursor-pointer"
                onClick={() => requestSort("title")}
              >
                Название {getSortIcon("title")}
              </th>
              <th
                className="px-4 py-2 cursor-pointer"
                onClick={() => requestSort("calories")}
              >
                Калории {getSortIcon("calories")}
              </th>
              <th
                className="px-4 py-2 cursor-pointer"
                onClick={() => requestSort("time")}
              >
                Время {getSortIcon("time")}
              </th>
              <th
                className="px-4 py-2 cursor-pointer"
                onClick={() => requestSort("createdAt")}
              >
                Дата {getSortIcon("createdAt")}
              </th>
            </tr>
          </thead>
        </table>
      </div>
    </div>
  );
};
