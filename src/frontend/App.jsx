const { useState, useEffect } = React;

function App() {
  const [twin, setTwin] = useState(null);
  const [messages, setMessages] = useState([
    { sender: "twin", text: "Hey! Upload your corpus or chat with my default Rivers Twin. I'll imitate their stylometrics and vocabulary metrics exactly! 🚀" }
  ]);
  const [inputText, setInputText] = useState("");
  const [selectedExplanation, setSelectedExplanation] = useState(null);
  const [loading, setLoading] = useState(false);

  // Default mock profile
  const mockTwinId = "64f1b2c3d4e5f6a7b8c9d0e1";

  useEffect(() => {
    fetchProfile(mockTwinId);
  }, []);

  const fetchProfile = async (id) => {
    try {
      const res = await fetch(`http://127.0.0.1:8000/api/v1/twin/${id}/profile`);
      if (res.ok) {
        const data = await res.json();
        setTwin(data);
      }
    } catch (err) {
      console.warn("FastAPI backend not running yet. Using client-side mock fallback.");
      // Client-side fallback so the dashboard works standalone
      setTwin({
        id: mockTwinId,
        username: "Alex Rivers",
        personality_profile: {
          big_five: { openness: 0.85, conscientiousness: 0.62, extraversion: 0.74, agreeableness: 0.78, neuroticism: 0.38 },
          stylometrics: { mean_sentence_length: 14.5, exclamation_rate: 0.03, top_emojis: ["🚀", "🔥", "💡"], ellipse_rate: 0.01 },
          frequent_vocabulary: [
            { word: "absolutely", count: 48 },
            { word: "innovative", count: 35 },
            { word: "strategy", count: 29 },
            { word: "dynamic", count: 22 },
            { word: "leverage", count: 18 }
          ]
        }
      });
    }
  };

  const handleSendMessage = async (e) => {
    e.preventDefault();
    if (!inputText.trim()) return;

    const userMsg = { sender: "user", text: inputText };
    setMessages(prev => [...prev, userMsg]);
    setInputText("");
    setLoading(true);

    try {
      const res = await fetch(`http://127.0.0.1:8000/api/v1/twin/${twin?.id || mockTwinId}/chat`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ message: inputText })
      });
      
      if (res.ok) {
        const data = await res.json();
        setMessages(prev => [...prev, {
          sender: "twin",
          text: data.response,
          explanation: data.explanation
        }]);
      } else {
        throw new Error("API Offline");
      }
    } catch (err) {
      console.error("Fetch error, running fallback:", err);
      // Mock generated fallback if backend offline
      setTimeout(() => {
        const profile = twin?.personality_profile;
        const words = profile?.frequent_vocabulary?.map(v => v.word) || ["absolutely", "innovative"];
        const ems = (profile?.stylometrics?.top_emojis || []).join("") || "🚀";
        const fallbackText = `I absolutely agree with that. We must leverage our ${words[1] || 'innovative'} strategy to push boundaries! ${ems}`;
        
        setMessages(prev => [...prev, {
          sender: "twin",
          text: fallbackText,
          explanation: {
            confidence_score: 0.88,
            influential_tokens: [
              { token: "absolutely", frequency_in_dataset: 48, attribution_weight: 0.96 },
              { token: "strategy", frequency_in_dataset: 29, attribution_weight: 0.58 }
            ],
            reasoning: "Generated output mirrors vocabulary patterns. Length compatibility matched at 85%."
          }
        }]);
      }, 700);
    } finally {
      setTimeout(() => {
        setLoading(false);
      }, 750);
    }
  };

  const handleFileUpload = async (e) => {
    const file = e.target.files[0];
    if (!file) return;
    const formData = new FormData();
    formData.append("file", file);

    try {
      const res = await fetch("http://127.0.0.1:8000/api/v1/twin/upload", {
        method: "POST",
        body: formData
      });
      if (res.ok) {
        const data = await res.json();
        setTwin(data);
        alert(`Successfully analyzed ${file.name}! Active Twin changed to: ${data.username}`);
      }
    } catch (err) {
      alert("Backend offline. Could not upload file.");
    }
  };

  return (
    <div className="min-h-screen bg-slate-100 text-slate-800 flex flex-col selection:bg-cyan-500/20 font-sans">
      {/* Header */}
      <header className="border-b border-slate-350 bg-white px-6 py-4 flex items-center justify-between sticky top-0 z-50 shadow-sm">
        <div className="flex items-center space-x-3">
          <div className="w-10 h-10 rounded-xl bg-gradient-to-tr from-cyan-500 to-indigo-650 flex items-center justify-center font-bold text-lg shadow-md text-white">
            DT
          </div>
          <div>
            <h1 className="font-extrabold text-lg tracking-tight text-slate-900">Digital Personality Twin</h1>
            <p className="text-xs text-slate-550 font-bold">Generative Persona Mirroring Engine</p>
          </div>
        </div>
        <div className="flex items-center space-x-4">
          <label className="cursor-pointer bg-white hover:bg-slate-50 text-slate-800 text-xs font-bold px-4 py-2.5 rounded-xl transition border-2 border-slate-350 hover:border-cyan-500/60 shadow-sm flex items-center space-x-2">
            <span>Upload Chat Log (.txt)</span>
            <input type="file" className="hidden" onChange={handleFileUpload} accept=".txt" />
          </label>
        </div>
      </header>

      {/* Main Workspace */}
      <main className="flex-1 max-w-7xl w-full mx-auto p-6 grid grid-cols-1 lg:grid-cols-12 gap-6">
        
        {/* Left Side: Personality & Stylometrics Analytics */}
        <section className="lg:col-span-5 space-y-6">
          
          {/* Twin Metadata */}
          <div className="bg-white border-2 border-slate-200 rounded-2xl p-6 shadow-sm relative overflow-hidden border-l-8 border-l-cyan-500">
            <span className="text-[10px] tracking-wider uppercase font-bold text-cyan-800 px-2.5 py-1 bg-cyan-50 border border-cyan-155 rounded-full inline-block">
              Active Personality Model
            </span>
            <h2 className="text-3xl font-black mt-3 text-slate-900 tracking-tight">{twin ? twin.username : "Loading..."}</h2>
            <p className="text-xs text-slate-600 mt-1.5 flex items-center space-x-1.5 font-bold">
              <span className="w-2 h-2 bg-cyan-500 rounded-full animate-ping" />
              <span>Learned from structural chat archives</span>
            </p>
          </div>

          {/* Big Five Personality Map */}
          <div className="bg-white border-2 border-slate-200 rounded-2xl p-6 shadow-sm flex flex-col relative overflow-hidden">
            <h3 className="font-bold text-xs tracking-wider text-slate-500 uppercase mb-4">Big Five Personality Traits</h3>
            <div className="space-y-4">
              {twin && Object.entries(twin.personality_profile.big_five).map(([trait, val]) => (
                <div key={trait}>
                  <div className="flex justify-between text-xs font-bold mb-1">
                    <span className="capitalize text-slate-800">{trait}</span>
                    <span className="text-indigo-650 font-black">{(val * 100).toFixed(0)}%</span>
                  </div>
                  <div className="h-3 w-full bg-slate-100 rounded-full border border-slate-200 overflow-hidden">
                    <div className="h-full bg-gradient-to-r from-cyan-500 to-indigo-600 rounded-full" style={{ width: `${val * 100}%` }} />
                  </div>
                </div>
              ))}
            </div>
          </div>

          {/* Stylometrics & Vocabulary */}
          <div className="bg-white border-2 border-slate-200 rounded-2xl p-6 shadow-sm relative overflow-hidden">
            <h3 className="font-bold text-xs tracking-wider text-slate-550 uppercase mb-4">Stylometric Signatures</h3>
            {twin && (
              <div className="grid grid-cols-2 gap-4 mb-5">
                <div className="bg-slate-50 p-4 rounded-xl border-2 border-slate-150 hover:border-cyan-500 transition group">
                  <span className="text-[10px] text-slate-500 block uppercase font-bold tracking-wide">Avg Sentence Length</span>
                  <span className="text-2xl font-black text-slate-900 mt-1 block">{twin.personality_profile.stylometrics.mean_sentence_length || 0} <span className="text-xs font-normal text-slate-500">words</span></span>
                </div>
                <div className="bg-slate-50 p-4 rounded-xl border-2 border-slate-150 hover:border-indigo-500 transition group">
                  <span className="text-[10px] text-slate-500 block uppercase font-bold tracking-wide">Signature Emojis</span>
                  <span className="text-2xl mt-1 block tracking-wider font-extrabold">{(twin.personality_profile.stylometrics.top_emojis || []).join(" ") || "🚀"}</span>
                </div>
              </div>
            )}

            <h4 className="font-bold text-[10px] tracking-wider uppercase text-slate-555 mb-3 border-t-2 border-slate-100 pt-4">Top Dataset Vocabulary</h4>
            <div className="flex flex-wrap gap-2">
              {twin && twin.personality_profile.frequent_vocabulary.map((vocab, i) => (
                <span key={i} className="bg-white border-2 border-slate-200 hover:border-indigo-500/50 hover:bg-indigo-50 px-3.5 py-1.5 rounded-full text-xs font-bold transition cursor-pointer text-slate-700 flex items-center space-x-1.5 shadow-sm">
                  <span>{vocab.word}</span>
                  <span className="bg-indigo-50 text-indigo-750 font-black px-1.5 py-0.5 rounded-full text-[10px] border border-indigo-150">{vocab.count}</span>
                </span>
              ))}
            </div>
          </div>
        </section>

        {/* Right Side: Chat & Explainability Interface */}
        <section className="lg:col-span-7 flex flex-col bg-white border-2 border-slate-200 rounded-2xl shadow-sm overflow-hidden min-h-[500px]">
          
          {/* Chat Window Header */}
          <div className="bg-slate-50 border-b-2 border-slate-200 px-6 py-4 flex items-center justify-between">
            <div className="flex items-center space-x-2">
              <span className="w-3 h-3 rounded-full bg-emerald-500 animate-pulse" />
              <span className="font-bold text-sm text-slate-700">Twin Simulation Instance</span>
            </div>
            {selectedExplanation && (
              <button onClick={() => setSelectedExplanation(null)} className="text-xs text-rose-650 font-extrabold hover:underline">
                Close Attribution Details
              </button>
            )}
          </div>

          <div className="flex-1 flex overflow-hidden">
            {/* Conversations List */}
            <div className="flex-1 p-6 overflow-y-auto space-y-4 max-h-[420px] bg-slate-50/40">
              {messages.map((msg, idx) => (
                <div key={idx} className={`flex items-start space-x-3.5 ${msg.sender === "user" ? "flex-row-reverse space-x-reverse" : "flex-row"}`}>
                  
                  {/* Avatar Icon */}
                  <div className={`w-9 h-9 rounded-full flex items-center justify-center text-[10px] font-black tracking-wider shrink-0 border-2 shadow-sm ${msg.sender === "user" ? "bg-slate-900 text-white border-slate-950" : "bg-cyan-500 text-white border-cyan-600"}`}>
                    {msg.sender === "user" ? "YOU" : "TWIN"}
                  </div>

                  {/* Message Speech Bubble */}
                  <div className={`max-w-[75%] rounded-2xl p-4 text-sm shadow-sm border-2 ${msg.sender === "user" ? "bg-slate-900 text-white rounded-tr-none border-slate-950 shadow-md" : "bg-white text-slate-800 rounded-tl-none border-slate-300 border-l-4 border-l-cyan-500"}`}>
                    {msg.sender === "twin" && (
                      <span className="text-[9px] font-black uppercase tracking-widest text-cyan-600 block mb-1.5">Simulated Response</span>
                    )}
                    <p className="leading-relaxed font-bold">{msg.text}</p>
                    {msg.explanation && (
                      <button 
                        onClick={() => setSelectedExplanation(msg.explanation)} 
                        className="text-[10px] text-indigo-650 font-extrabold hover:underline block mt-3 border-t border-slate-100 pt-2.5 w-full text-left"
                      >
                        ✨ Explain why this was generated
                      </button>
                    )}
                  </div>
                </div>
              ))}
              {loading && (
                <div className="flex items-start space-x-3.5">
                  <div className="w-9 h-9 rounded-full bg-cyan-500 text-white border-2 border-cyan-600 flex items-center justify-center text-[10px] font-black shrink-0 animate-pulse">
                    TWIN
                  </div>
                  <div className="bg-white text-slate-500 text-xs px-4 py-3.5 rounded-2xl rounded-tl-none flex items-center space-x-1.5 shadow-sm border-2 border-slate-300 border-l-4 border-l-cyan-500">
                    <span className="font-bold">Analyzing stylometrics</span>
                    <span className="w-1.5 h-1.5 bg-cyan-500 rounded-full animate-bounce" style={{ animationDelay: '0ms' }} />
                    <span className="w-1.5 h-1.5 bg-cyan-500 rounded-full animate-bounce" style={{ animationDelay: '150ms' }} />
                    <span className="w-1.5 h-1.5 bg-cyan-500 rounded-full animate-bounce" style={{ animationDelay: '300ms' }} />
                  </div>
                </div>
              )}
            </div>

            {/* XAI Attribution Drawer */}
            {selectedExplanation && (
              <div className="w-72 border-l-2 border-slate-200 bg-slate-50 p-5 space-y-5 overflow-y-auto">
                <h4 className="font-bold text-xs uppercase tracking-widest text-indigo-750 flex items-center space-x-1.5">
                  <span>✨ Attribution Analysis</span>
                </h4>
                <div className="bg-white p-3 rounded-xl border-2 border-slate-200 shadow-sm">
                  <span className="text-[10px] text-slate-500 block uppercase font-bold">Style Similarity</span>
                  <span className="text-3xl font-black text-slate-900 mt-1 block">{(selectedExplanation.confidence_score * 100).toFixed(0)}%</span>
                </div>
                <div className="space-y-3">
                  <span className="text-[10px] text-slate-500 block uppercase font-bold">Influencing Tokens</span>
                  <div className="space-y-2">
                    {selectedExplanation.influential_tokens.map((tok, idx) => (
                      <div key={idx} className="bg-white border-2 border-slate-200 p-3 rounded-xl text-xs hover:border-cyan-500 transition shadow-sm">
                        <div className="flex justify-between font-bold mb-1">
                          <span className="text-slate-800">"{tok.token}"</span>
                          <span className="text-cyan-750 font-black">{(tok.attribution_weight * 100).toFixed(0)}% weight</span>
                        </div>
                        <span className="text-[10px] text-slate-500">Matched {tok.frequency_in_dataset} times in corpus</span>
                      </div>
                    ))}
                  </div>
                </div>
                <div className="text-[10px] text-slate-550 border-t-2 border-slate-200 pt-4">
                  <strong>Reasoning:</strong> {selectedExplanation.reasoning}
                </div>
              </div>
            )}
          </div>

          {/* Form input */}
          <form onSubmit={handleSendMessage} className="p-4 bg-slate-50 border-t-2 border-slate-200 flex gap-2">
            <input
              type="text"
              value={inputText}
              onChange={(e) => setInputText(e.target.value)}
              placeholder="Type a message to your twin..."
              className="flex-1 bg-white border-2 border-slate-250 rounded-xl px-4 py-3.5 text-sm focus:outline-none focus:border-cyan-500 transition text-slate-900 placeholder-slate-400 shadow-sm font-bold"
            />
            <button type="submit" className="bg-gradient-to-r from-cyan-600 to-indigo-650 hover:from-cyan-700 hover:to-indigo-750 text-white font-bold text-sm px-6 py-3.5 rounded-xl transition shadow-md shadow-indigo-500/15">
              Send
            </button>
          </form>
        </section>

      </main>
    </div>
  );
}

const root = ReactDOM.createRoot(document.getElementById("root"));
root.render(<App />);