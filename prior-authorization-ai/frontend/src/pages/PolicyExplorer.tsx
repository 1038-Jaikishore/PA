import React, { useState } from 'react';

export const PolicyExplorer = () => {
  const [icd10, setIcd10] = useState('M17.11');
  const [hcpcs, setHcpcs] = useState('97110');
  const [stateInput, setStateInput] = useState('');
  const [loading, setLoading] = useState(false);
  const [result, setResult] = useState<any>(null);
  const [error, setError] = useState<string | null>(null);

  const handleResolve = async (e: React.FormEvent) => {
    e.preventDefault();
    setLoading(true);
    setError(null);
    setResult(null);

    try {
      const response = await fetch('/api/policies/resolve', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ icd10, hcpcs_cpt: hcpcs, state: stateInput })
      });

      if (!response.ok) {
        throw new Error(`Error: ${response.statusText}`);
      }
      
      const data = await response.json();
      setResult(data);
    } catch (err: any) {
      setError(err.message || 'An error occurred during resolution');
    } finally {
      setLoading(false);
    }
  };

  const renderArticleNode = (articleData: any) => {
    if (!articleData) return null;
    return (
      <div className="p-4 border rounded bg-indigo-50/10 mb-4 shadow-sm border-indigo-200/20">
        <div className="flex justify-between items-start">
          <div>
            <span className="text-xs font-mono bg-indigo-900/40 text-indigo-200 px-2 py-1 rounded">Article</span>
            <h4 className="font-bold text-lg mt-1">{articleData.title}</h4>
            <div className="text-sm opacity-80 mt-1">ID: {articleData.article_id?.display_value || articleData.article_id} | Ver: {articleData.article_version}</div>
          </div>
          <div className="text-xs font-mono bg-gray-900/50 text-gray-400 px-2 py-1 rounded border border-gray-700">
            _id: {articleData._id}
          </div>
        </div>
      </div>
    );
  };

  const renderLcdNode = (lcdNode: any) => {
    const lcdData = lcdNode.lcd;
    if (!lcdData) return null;
    return (
      <div className="ml-8 p-4 border rounded bg-emerald-50/10 mb-4 shadow-sm border-emerald-200/20 relative">
        {/* Connector line */}
        <div className="absolute -left-8 top-6 w-8 h-px bg-emerald-500/30"></div>
        <div className="absolute -left-8 -top-full h-full w-px bg-emerald-500/30"></div>
        
        <div className="flex justify-between items-start">
          <div>
            <span className="text-xs font-mono bg-emerald-900/40 text-emerald-200 px-2 py-1 rounded">LCD</span>
            <h4 className="font-bold text-lg mt-1">{lcdData.title}</h4>
            <div className="text-sm opacity-80 mt-1">ID: {lcdData.lcd_id?.display_value || lcdData.lcd_id} | Ver: {lcdData.lcd_version}</div>
          </div>
          <div className="text-xs font-mono bg-gray-900/50 text-gray-400 px-2 py-1 rounded border border-gray-700">
            _id: {lcdData._id}
          </div>
        </div>
        
        {/* Render NCDs inside LCD */}
        <div className="mt-4">
          {lcdNode.ncds && lcdNode.ncds.map((ncdNode: any, idx: number) => renderNcdNode(ncdNode, idx))}
        </div>
      </div>
    );
  };

  const renderNcdNode = (ncdNode: any, idx: number) => {
    if (ncdNode.status === 'NO_RELATED_NCD') {
      return (
        <div key={idx} className="ml-8 p-3 border rounded border-dashed border-gray-600 bg-gray-800/30 text-sm text-gray-400 mb-2 relative">
          <div className="absolute -left-8 top-5 w-8 h-px bg-gray-600/30"></div>
          Status: No valid NCD link found (value: {ncdNode.raw_relation?.r_ncd_id || '0'})
        </div>
      );
    }
    
    const ncdData = ncdNode.ncd;
    if (!ncdData) return null;
    
    return (
      <div key={idx} className="ml-8 p-4 border rounded bg-amber-50/10 mb-2 shadow-sm border-amber-200/20 relative">
        <div className="absolute -left-8 top-6 w-8 h-px bg-amber-500/30"></div>
        
        <div className="flex justify-between items-start">
          <div>
            <span className="text-xs font-mono bg-amber-900/40 text-amber-200 px-2 py-1 rounded">NCD</span>
            <h4 className="font-bold text-lg mt-1">{ncdData.title}</h4>
            <div className="text-sm opacity-80 mt-1">ID: {ncdData.ncd_id?.display_value || ncdData.ncd_id}</div>
          </div>
          <div className="text-xs font-mono bg-gray-900/50 text-gray-400 px-2 py-1 rounded border border-gray-700">
            _id: {ncdData._id}
          </div>
        </div>
      </div>
    );
  };

  const renderGraph = (graph: any, type: 'covered' | 'non_covered') => {
    const isCovered = type === 'covered';
    return (
      <div className={`mb-8 p-6 rounded-xl border-l-4 ${isCovered ? 'border-l-emerald-500 bg-gradient-to-br from-emerald-900/20 to-transparent' : 'border-l-rose-500 bg-gradient-to-br from-rose-900/20 to-transparent'}`}>
        <h3 className="text-xl font-bold mb-4 flex items-center gap-2">
          {isCovered ? (
            <><span className="w-3 h-3 rounded-full bg-emerald-500"></span> Covered Article Track</>
          ) : (
            <><span className="w-3 h-3 rounded-full bg-rose-500"></span> Non-Covered Article Track</>
          )}
        </h3>
        
        {renderArticleNode(graph.article)}
        
        <div className="pl-4">
          {graph.lcds && graph.lcds.length > 0 ? (
            graph.lcds.map((lcdNode: any, idx: number) => (
              <div key={idx}>{renderLcdNode(lcdNode)}</div>
            ))
          ) : (
            <div className="ml-8 text-sm text-gray-500 italic">No associated LCDs found for this article.</div>
          )}
        </div>
      </div>
    );
  };

  return (
    <div className="animate-fade-in max-w-6xl mx-auto space-y-6 pb-20">
      <header className="mb-8">
        <h1 className="text-4xl font-bold bg-clip-text text-transparent bg-gradient-to-r from-blue-400 to-emerald-400">
          Policy Explorer
        </h1>
        <p className="text-white/60 mt-2 text-lg">
          Deterministic CMS Policy Relationship Engine (Volume 3)
        </p>
      </header>

      <div className="glass-panel p-6 border-l-4 border-l-blue-500">
        <h2 className="text-xl font-bold mb-4">Resolution Engine Query</h2>
        <form onSubmit={handleResolve} className="grid grid-cols-1 md:grid-cols-4 gap-4 items-end">
          <div>
            <label className="block text-sm font-medium text-gray-400 mb-1">ICD-10 Code</label>
            <input 
              type="text" 
              value={icd10} 
              onChange={e => setIcd10(e.target.value)}
              className="w-full bg-gray-900/50 border border-gray-700 rounded-lg px-4 py-2 focus:ring-2 focus:ring-blue-500 focus:border-transparent outline-none transition-all text-white placeholder-gray-500"
              placeholder="e.g. M17.11"
              required
            />
          </div>
          <div>
            <label className="block text-sm font-medium text-gray-400 mb-1">HCPCS / CPT Code</label>
            <input 
              type="text" 
              value={hcpcs} 
              onChange={e => setHcpcs(e.target.value)}
              className="w-full bg-gray-900/50 border border-gray-700 rounded-lg px-4 py-2 focus:ring-2 focus:ring-blue-500 focus:border-transparent outline-none transition-all text-white placeholder-gray-500"
              placeholder="e.g. 97110"
              required
            />
          </div>
          <div>
            <label className="block text-sm font-medium text-gray-400 mb-1">State (Optional)</label>
            <input 
              type="text" 
              value={stateInput} 
              onChange={e => setStateInput(e.target.value)}
              className="w-full bg-gray-900/50 border border-gray-700 rounded-lg px-4 py-2 focus:ring-2 focus:ring-blue-500 focus:border-transparent outline-none transition-all text-white placeholder-gray-500"
              placeholder="e.g. TX"
            />
          </div>
          <div>
            <button 
              type="submit" 
              disabled={loading}
              className="w-full bg-gradient-to-r from-blue-600 to-indigo-600 hover:from-blue-500 hover:to-indigo-500 text-white font-medium py-2 px-4 rounded-lg shadow-lg shadow-blue-500/20 transition-all disabled:opacity-50"
            >
              {loading ? 'Resolving...' : 'Resolve Policy Tree'}
            </button>
          </div>
        </form>
      </div>

      {error && (
        <div className="glass-panel p-4 bg-red-500/10 border border-red-500/30 text-red-200">
          <p className="font-medium">Error Resolution Failed</p>
          <p className="text-sm opacity-80 mt-1">{error}</p>
        </div>
      )}

      {result && (
        <div className="space-y-6 animate-fade-in">
          {/* Intermediate Stats */}
          <div className="grid grid-cols-2 md:grid-cols-5 gap-4">
            <div className="glass-panel p-4 text-center">
              <div className="text-3xl font-light text-blue-400">{result.intermediate_results.icd_covered_count}</div>
              <div className="text-xs text-gray-400 uppercase tracking-wider mt-1">ICD Covered</div>
            </div>
            <div className="glass-panel p-4 text-center">
              <div className="text-3xl font-light text-rose-400">{result.intermediate_results.icd_non_covered_count}</div>
              <div className="text-xs text-gray-400 uppercase tracking-wider mt-1">ICD Non-Covered</div>
            </div>
            <div className="glass-panel p-4 text-center">
              <div className="text-3xl font-light text-indigo-400">{result.intermediate_results.hcpcs_article_count}</div>
              <div className="text-xs text-gray-400 uppercase tracking-wider mt-1">HCPCS Articles</div>
            </div>
            <div className="glass-panel p-4 text-center border border-emerald-500/30 shadow-[0_0_15px_rgba(16,185,129,0.1)]">
              <div className="text-3xl font-bold text-emerald-400">{result.intermediate_results.intersected_covered_count}</div>
              <div className="text-xs text-emerald-400/80 uppercase tracking-wider mt-1">Covered Hits</div>
            </div>
            <div className="glass-panel p-4 text-center border border-rose-500/30 shadow-[0_0_15px_rgba(244,63,94,0.1)]">
              <div className="text-3xl font-bold text-rose-400">{result.intermediate_results.intersected_non_covered_count}</div>
              <div className="text-xs text-rose-400/80 uppercase tracking-wider mt-1">Non-Covered Hits</div>
            </div>
          </div>

          <div className="glass-panel p-8 relative overflow-hidden">
            <div className="absolute top-0 right-0 p-4">
              <span className="inline-flex items-center px-3 py-1 rounded-full text-xs font-medium bg-gray-800 text-gray-300 border border-gray-700">
                Status: {result.jurisdiction_status.replace(/_/g, ' ')}
              </span>
            </div>
            
            <h2 className="text-2xl font-bold mb-8">Resolution Graph</h2>
            
            {result.resolved_policies.covered.length === 0 && result.resolved_policies.non_covered.length === 0 && (
              <div className="text-center py-12 text-gray-500">
                <div className="text-4xl mb-3 opacity-30">🔍</div>
                <p>No policy intersection found for this ICD-10 and HCPCS combination.</p>
              </div>
            )}
            
            {result.resolved_policies.covered.map((graph: any, i: number) => (
              <React.Fragment key={`cov-${i}`}>
                {renderGraph(graph, 'covered')}
              </React.Fragment>
            ))}
            
            {result.resolved_policies.non_covered.map((graph: any, i: number) => (
              <React.Fragment key={`ncov-${i}`}>
                {renderGraph(graph, 'non_covered')}
              </React.Fragment>
            ))}
          </div>
        </div>
      )}
    </div>
  );
};
