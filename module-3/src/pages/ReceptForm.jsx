import { useEffect, useState } from "react";
import { useNavigate, useParams } from "react-router-dom";

export const ReceptForm = () => {
  const { id, still_id } = useParams();
  console.log(id, still_id)
  const [categoty, setCategory] = useState([]);
  const [errors, setErrors] = useState({});
  const [form, setForm] = useState({
    title: "",
    decription: "",
    hours: "",
    status: "",
    category: "",
    price: "",
    photos: [],
  });
  const navigate = useNavigate();

  useEffect(() => {
    const fetchData = async () => {
      const token = localStorage.getItem("token");
      const response = await fetch("http://127.0.0.1:8000/api/category", {
        headers: {
          "Content-Type": "application/json",
          Authorization: `Bearer ${token}`,
        },
      });
      if (response.ok) {
        const result = await response.json();
        setCategory(result);
      }
    };
    fetchData();
  }, []);

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      const token = localStorage.getItem("token");
      const response = await fetch("http://127.0.0.1:8000/api/recepts", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
          Authorization: `Bearer ${token}`,
        },
        body: JSON.stringify(form),
      });
      if (response.ok) {
        navigate("/");
      } else {
        const result = await response.json();
        setErrors(result.error);
      }
    } catch (e) {
      console.error(e);
    }
    console.log(form);
  };
  return (
    <form action="" onSubmit={handleSubmit}>
      <input
        type="text"
        value={form.title}
        onChange={(e) => setForm({ ...form, [e.target.name]: e.target.value })}
        name="title"
        placeholder="title"
      />
      {errors.title && <p className="text-red-600">{errors.title}</p>}
      <input
        type="text"
        value={form.decription}
        onChange={(e) => setForm({ ...form, [e.target.name]: e.target.value })}
        name="decription"
        placeholder="decription"
      />
      {errors.decription && <p className="text-red-600">{errors.decription}</p>}
      <input
        type="text"
        value={form.hours}
        onChange={(e) => setForm({ ...form, [e.target.name]: e.target.value })}
        name="hours"
        placeholder="hours"
      />
      {errors.hours && <p className="text-red-600">{errors.hours}</p>}
      <input
        type="text"
        value={form.price}
        onChange={(e) => setForm({ ...form, [e.target.name]: e.target.value })}
        name="price"
        placeholder="price"
      />
      {errors.price && <p className="text-red-600">{errors.price}</p>}

      <select
        name="status"
        onChange={(e) => setForm({ ...form, [e.target.name]: e.target.value })}
      >
        <option value="easy">Легко</option>
        <option value="medium">Средне</option>
        <option value="hard">Сложно</option>
      </select>
      {errors.status && <p className="text-red-600">{errors.status}</p>}
      <select
        name="category"
        value={form.category}
        onChange={(e) =>
          setForm({ ...form, [e.target.name]: Number(e.target.value) })
        }
      >
        <option value="" disabled>
          Выберите категорию
        </option>
        {categoty.map((item) => (
          <option value={item.id}>{item.title}</option>
        ))}
      </select>

      <button>Отправить</button>
    </form>
  );
};
