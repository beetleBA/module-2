import { useState } from 'react';

const CreateRecipe = () => {
  const [form, setForm] = useState({
    title: '',
    description: '',
    calories: '',
    time: '',
  });
  const [image, setImage] = useState(null);  // ← Отдельное состояние для файла
  const [loading, setLoading] = useState(false);

  const handleChange = (e) => {
    setForm({ ...form, [e.target.name]: e.target.value });
  };

  const handleImage = (e) => {
    setImage(e.target.files[0]);  // ← File объект
  };

  const submitRecipe = async (e) => {
    e.preventDefault();
    setLoading(true);

    // ✅ FormData для файлов!
    const formData = new FormData();
    formData.append('title', form.title);
    formData.append('description', form.description);
    formData.append('calories', form.calories);
    formData.append('time', form.time);
    formData.append('image', image);  // ← Файл!

    try {
      const res = await fetch('http://localhost:8000/api/recipes/', {
        method: 'POST',
        body: formData,  // ← НЕ JSON.stringify!
        // ❌ НЕ headers: {'Content-Type': 'application/json'}
        // ✅ Browser сам ставит multipart/form-data + boundary
      });
      
      if (res.ok) {
        alert('Рецепт создан!');
        // navigate('/') или обновить список
      } else {
        const error = await res.json();
        console.error(error);
      }
    } catch (err) {
      console.error('Ошибка:', err);
    }
    setLoading(false);
  };

  return (
    <form onSubmit={submitRecipe} className="max-w-md mx-auto p-6">
      <input name="title" onChange={handleChange} placeholder="Название" className="block w-full mb-4 p-2 border" />
      <textarea name="description" onChange={handleChange} placeholder="Описание" className="block w-full mb-4 p-2 border" />
      <input name="calories" type="number" onChange={handleChange} placeholder="Калории" className="block w-full mb-4 p-2 border" />
      <input name="time" type="number" onChange={handleChange} placeholder="Время (мин)" className="block w-full mb-4 p-2 border" />
      
      {/* ✅ File input */}
      <input 
        type="file" 
        accept="image/*" 
        onChange={handleImage}
        className="block w-full mb-4"
      />
      
      <button type="submit" disabled={loading} className="w-full bg-blue-500 text-white p-2 rounded">
        {loading ? 'Загрузка...' : 'Создать рецепт'}
      </button>
    </form>
  );
};