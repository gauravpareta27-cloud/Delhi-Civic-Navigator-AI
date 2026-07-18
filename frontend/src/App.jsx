import React from 'react';
import ChatInterface from './components/ChatInterface';

function App() {
  return (
    <div className="min-h-screen relative overflow-hidden bg-dark-900 pb-20">
      {/* Background decorations */}
      <div className="absolute top-0 left-0 w-full h-96 bg-gradient-to-b from-primary-900/20 to-transparent pointer-events-none"></div>
      <div className="absolute top-[-20%] left-[-10%] w-[50%] h-[50%] rounded-full bg-primary-600/10 blur-[120px] pointer-events-none"></div>
      <div className="absolute bottom-[-10%] right-[-10%] w-[40%] h-[40%] rounded-full bg-blue-600/10 blur-[100px] pointer-events-none"></div>
      
      {/* Main Content */}
      <main className="relative z-10 px-4 sm:px-6 lg:px-8 max-w-7xl mx-auto flex flex-col items-center min-h-screen">
        <ChatInterface />
      </main>
      
      {/* Footer */}
      <footer className="absolute bottom-4 w-full text-center text-gray-500 text-sm font-medium z-10">
        <p>Built for the 4-Hour Hackathon • Data sourced from official Delhi Government portals</p>
      </footer>
    </div>
  );
}

export default App;
