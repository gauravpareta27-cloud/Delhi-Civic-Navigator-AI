import React from 'react';
import ReactMarkdown from 'react-markdown';
import { CheckCircle2, Clock, MapPin, Building2, ExternalLink, IndianRupee } from 'lucide-react';

const ServiceResult = ({ result }) => {
  if (!result) return null;

  // Basic parsing of the structured response from LLM
  // Since the LLM returns structured text, we will parse it to render UI components nicely
  const parseSection = (title) => {
    const regex = new RegExp(`${title}:\n([\\s\\S]*?)(?=\n\n[A-Z][a-z]+:|$)`, 'i');
    const match = result.match(regex);
    return match ? match[1].trim() : null;
  };

  const service = parseSection('Service');
  const department = parseSection('Department');
  const eligibility = parseSection('Eligibility');
  const docs = parseSection('Required Documents');
  const fees = parseSection('Fees');
  const time = parseSection('Processing Time');
  const steps = parseSection('How to Apply');
  const source = parseSection('Official Source');

  // If the LLM returned the fallback message
  if (result.includes("I'm sorry")) {
    return (
      <div className="glass-panel p-6 mt-6 animate-slide-up border-red-500/30">
        <p className="text-gray-300">{result}</p>
      </div>
    );
  }

  return (
    <div className="glass-panel p-8 mt-8 animate-slide-up space-y-8">
      {/* Header */}
      <div className="border-b border-gray-700/50 pb-6">
        <h2 className="text-3xl font-bold bg-gradient-to-r from-primary-400 to-primary-600 bg-clip-text text-transparent">
          {service || 'Service Details'}
        </h2>
        {department && (
          <div className="flex items-center text-gray-400 mt-2 gap-2 font-medium">
            <Building2 size={18} className="text-primary-500" />
            {department}
          </div>
        )}
      </div>

      {/* Grid for Quick Stats */}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
        <div className="bg-dark-900/50 p-4 rounded-xl border border-gray-700/30 flex items-start gap-3">
          <Clock className="text-primary-500 mt-1" size={20} />
          <div>
            <p className="text-sm text-gray-500 font-medium">Processing Time</p>
            <p className="font-semibold text-gray-200 mt-1">{time || 'N/A'}</p>
          </div>
        </div>
        <div className="bg-dark-900/50 p-4 rounded-xl border border-gray-700/30 flex items-start gap-3">
          <IndianRupee className="text-primary-500 mt-1" size={20} />
          <div>
            <p className="text-sm text-gray-500 font-medium">Fees</p>
            <p className="font-semibold text-gray-200 mt-1">{fees || 'N/A'}</p>
          </div>
        </div>
        <div className="bg-dark-900/50 p-4 rounded-xl border border-gray-700/30 flex items-start gap-3 md:col-span-1">
          <MapPin className="text-primary-500 mt-1" size={20} />
          <div>
            <p className="text-sm text-gray-500 font-medium">Location</p>
            <p className="font-semibold text-gray-200 mt-1">Delhi, India</p>
          </div>
        </div>
      </div>

      {/* Eligibility */}
      {eligibility && (
        <div>
          <h3 className="text-lg font-semibold text-white mb-3 flex items-center gap-2">
            <CheckCircle2 size={20} className="text-primary-500" />
            Eligibility
          </h3>
          <p className="text-gray-300 leading-relaxed bg-dark-900/30 p-4 rounded-xl border border-gray-700/30">
            {eligibility}
          </p>
        </div>
      )}

      <div className="grid grid-cols-1 md:grid-cols-2 gap-8">
        {/* Documents */}
        {docs && (
          <div>
            <h3 className="text-lg font-semibold text-white mb-4">Required Documents</h3>
            <div className="bg-dark-900/30 p-5 rounded-xl border border-gray-700/30">
              <ReactMarkdown 
                className="prose prose-invert max-w-none prose-ul:list-disc prose-ul:pl-4 prose-li:text-gray-300 prose-li:marker:text-primary-500"
              >
                {docs}
              </ReactMarkdown>
            </div>
          </div>
        )}

        {/* Steps */}
        {steps && (
          <div>
            <h3 className="text-lg font-semibold text-white mb-4">How to Apply</h3>
            <div className="bg-dark-900/30 p-5 rounded-xl border border-gray-700/30 space-y-3">
              {steps.split('\n').filter(s => s.trim()).map((step, idx) => (
                <div key={idx} className="flex gap-3">
                  <div className="w-6 h-6 rounded-full bg-primary-600/20 text-primary-400 flex items-center justify-center shrink-0 text-sm font-bold border border-primary-500/30">
                    {idx + 1}
                  </div>
                  <p className="text-gray-300 text-sm leading-relaxed pt-0.5">
                    {step.replace(/^Step \d+:\s*/, '')}
                  </p>
                </div>
              ))}
            </div>
          </div>
        )}
      </div>

      {/* Source */}
      {source && (
        <div className="pt-4 border-t border-gray-700/50 flex items-center justify-between">
          <p className="text-sm text-gray-400 flex items-center gap-2">
            <span className="w-2 h-2 rounded-full bg-green-500 animate-pulse"></span>
            Information sourced from official government portal
          </p>
          <a 
            href={source} 
            target="_blank" 
            rel="noopener noreferrer"
            className="flex items-center gap-2 text-sm font-medium text-primary-400 hover:text-primary-300 transition-colors"
          >
            Visit Official Website
            <ExternalLink size={16} />
          </a>
        </div>
      )}
    </div>
  );
};

export default ServiceResult;
