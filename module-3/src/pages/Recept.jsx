import { useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";

export const Recept = () => {
  const navigate = useNavigate();
  const [data, setData] = useState([]);

  const fetchData = async () => {
    const token = localStorage.getItem("token");
    const response = await fetch("http://127.0.0.1:8000/api/recepts", {
      headers: {
        Authorization: `Bearer ${token}`,
      },
    });
    if (response.ok) {
      const result = await response.json();
      setData(result.data);
    }
  };
  useEffect(() => {
    fetchData();
  }, []);

  return (
    <div className="p-7">
      <button
        className="bg-blue-500 py-2 px-4 text-white rounded-full my-4"
        onClick={() => navigate('/recept/create')}
      >
        Добавить
      </button>
      {data.map((item) => (
        <div className="flex gap-5" key={item.id}>
          <p>{item.id}</p>
          <p>{item.title}</p>
          <p className="max-w-xl">{item.decription}</p>
          <p>{item.difficulty}</p>
          <p>{item.price}</p>
          <p>{item.category.title}</p>
          <p>{item.formatted_time}</p>
        </div>
      ))}
    </div>
  );
};
