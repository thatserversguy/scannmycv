"use client";  // 👈 Add this line at the very top

import { useState } from 'react';
import axios from 'axios';

export default function Home() {
  const [file, setFile] = useState(null);
  const [uploading, setUploading] = useState(false);
  const [result, setResult] = useState(null);

  const handleFileChange = (e) => {
    setFile(e.target.files[0]);
  };

  const handleUpload = async () => {
    if (!file) return;
    setUploading(true);

    const formData = new FormData();
    formData.append('file', file);

    try {
      const res = await axios.post('http://127.0.0.1:8000/upload', formData);
      setResult(res.data);
    } catch (err) {
      console.error('Upload failed', err);
    }

    setUploading(false);
  };

  return (
    <main className="min-h-screen p-8 bg-gray-100">
      <h1 className="text-2xl font-bold mb-4">ScannMyCV</h1>
      <input type="file" onChange={handleFileChange} className="mb-2" />
      <button onClick={handleUpload} className="bg-blue-600 text-white px-4 py-2 rounded">
        {uploading ? 'Uploading...' : 'Analyze Resume'}
      </button>

      {result && (
        <div className="mt-6">
          <h2 className="text-xl font-semibold">Analysis Result</h2>
          <pre className="bg-white p-4 rounded shadow mt-2">{JSON.stringify(result, null, 2)}</pre>
        </div>
      )}
    </main>
  );
}
