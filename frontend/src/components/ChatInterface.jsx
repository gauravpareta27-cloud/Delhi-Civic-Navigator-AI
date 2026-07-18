import React, { useState } from 'react';
import { Search, Loader2, Landmark } from 'lucide-react';
import ServiceResult from './ServiceResult';

const ChatInterface = () => {
  const [query, setQuery] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const [result, setResult] = useState(null);
  const [error, setError] = useState('');

  const handleSearch = async (e) => {
    e.preventDefault();
    if (!query.trim()) return;

    setIsLoading(true);
    setError('');
    setResult(null);

    try {
      const res = await fetch('http://localhost:8000/api/search', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ query }),
      });

      if (!res.ok) {
        throw new Error('Failed to fetch from server.');
      }

      const data = await res.json();
      setResult(data.response);
    } catch (err) {
      setError('Unable to reach the server. Make sure the FastAPI backend is running.');
    } finally {
      setIsLoading(false);
    }
  };

  const commonSearches = [
    "Birth Certificate",
    "Driving Licence",
    "Income Certificate",
    "Property Tax"
  ];

  return (
    <div className="w-full max-w-4xl mx-auto mt-12 animate-fade-in">
      
      <div className="text-center mb-10">
        <div className="inline-flex items-center justify-center p-4 bg-primary-600/10 rounded-2xl mb-6 shadow-[0_0_30px_rgba(34,197,94,0.15)] border border-primary-500/20">
          <Landmark size={48} className="text-primary-500" />
        </div>
        <h1 className="text-5xl font-extrabold tracking-tight mb-4 text-white">
          Delhi Civic <span className="text-transparent bg-clip-text bg-gradient-to-r from-primary-400 to-primary-600">Navigator AI</span>
        </h1>
        <p className="text-lg text-gray-400 max-w-2xl mx-auto font-medium">
          Get official document checklists, fees, and processing times for Delhi government services in seconds.
        </p>
      </div>

      <div className="glass-panel p-2 mb-8 mx-4 sm:mx-0 transition-transform focus-within:scale-[1.02] focus-within:shadow-[0_0_40px_rgba(34,197,94,0.1)]">
        <form onSubmit={handleSearch} className="flex gap-2 relative">
          <div className="relative flex-grow">
            <Search className="absolute left-4 top-1/2 -translate-y-1/2 text-gray-500" size={20} />
            <input
              type="text"
              value={query}
              onChange={(e) => setQuery(e.target.value)}
              placeholder="e.g. 'How to get a Birth Certificate?' or 'Driving Licence fees'"
              className="input-field pl-12 h-14 text-lg bg-transparent border-none shadow-none"
              autoFocus
            />
          </div>
          <button 
            type="submit" 
            disabled={isLoading || !query.trim()}
            className="btn-primary h-14 px-8 text-lg font-semibold disabled:opacity-50 disabled:cursor-not-allowed"
          >
            {isLoading ? <Loader2 className="animate-spin" size={24} /> : 'Search'}
          </button>
        </form>
      </div>

      {!result && !isLoading && (
        <div className="flex flex-wrap justify-center gap-3 px-4">
          <span className="text-sm text-gray-500 mt-2 mr-2 font-medium">Try searching:</span>
          {commonSearches.map(term => (
            <button
              key={term}
              onClick={() => setQuery(term)}
              className="px-4 py-2 rounded-full bg-dark-800 border border-gray-700/50 text-sm text-gray-300 hover:bg-dark-700 hover:text-white hover:border-primary-500/50 transition-all font-medium"
            >
              {term}
            </button>
          ))}
        </div>
      )}

      {error && (
        <div className="p-4 bg-red-900/20 border border-red-500/50 text-red-400 rounded-xl mt-6 text-center animate-slide-up mx-4 sm:mx-0">
          {error}
        </div>
      )}

      <ServiceResult result={result} />
    </div>
  );
};

export default ChatInterface;
