const { useState, useEffect, useRef } = React;

// --- LOGIN PAGE COMPONENT ---
function LoginPage({ onLogin }) {
  const [username, setUsername] = useState("");
  const [password, setPassword] = useState("");
  const [error, setError] = useState("");
  const [loading, setLoading] = useState(false);

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    setError("");
    try {
      const formData = new URLSearchParams();
      formData.append("username", username);
      formData.append("password", password);

      const res = await fetch("/api/auth/login-form", {
        method: "POST",
        headers: { "Content-Type": "application/x-www-form-urlencoded" },
        body: formData
      });
      if (res.ok) {
        const data = await res.json();
        onLogin(data);
      } else {
        setError("Invalid username or password");
      }
    } catch (err) {
      setError("Network error occurred");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="relative flex items-center justify-center min-h-screen font-sans overflow-hidden bg-[#0F172A]">
      {/* Background Image with Overlay */}
      <div
        className="absolute inset-0 z-0 bg-cover bg-center bg-no-repeat"
        style={{ backgroundImage: "url('/static/hero-bg.jpg')" }}
      >
        <div className="absolute inset-0 bg-gradient-to-r from-[#0F172A]/90 via-[#0F172A]/80 to-[#0F172A]/70"></div>
      </div>

      <div className="command-panel relative z-10 w-full max-w-md p-8 shadow-2xl border-t-4 border-t-[#2563EB] bg-white/95 backdrop-blur">
        <div className="text-center mb-8">
          <div className="inline-flex items-center justify-center w-20 h-20 bg-white rounded-xl shadow-sm border border-[#E2E8F0] mb-4 overflow-hidden">
            <img src="/static/logo.png" alt="Logo" className="w-full h-full object-cover" />
          </div>
          <h2 className="text-2xl font-black text-[#0F172A] tracking-tight">OIL-SAFE AI</h2>
          <p className="text-[#475569] text-sm mt-1">Industrial Safety Command Center</p>
        </div>

        {error && (
          <div className="mb-4 p-3 bg-[#FEF2F2] border border-[#FECACA] text-[#DC2626] rounded-md text-sm font-medium">
            {error}
          </div>
        )}

        <form onSubmit={handleSubmit} className="space-y-5">
          <div>
            <label className="block text-xs font-bold text-[#475569] uppercase mb-1">Username</label>
            <input
              type="text"
              className="w-full px-4 py-2 bg-white border border-[#CBD5E1] rounded-lg focus:outline-none focus:ring-2 focus:ring-[#2563EB] text-[#0F172A]"
              value={username}
              onChange={(e) => setUsername(e.target.value)}
              placeholder="e.g. safety_manager"
              required
            />
          </div>
          <div>
            <label className="block text-xs font-bold text-[#475569] uppercase mb-1">Password</label>
            <input
              type="password"
              className="w-full px-4 py-2 bg-white border border-[#CBD5E1] rounded-lg focus:outline-none focus:ring-2 focus:ring-[#2563EB] text-[#0F172A]"
              value={password}
              onChange={(e) => setPassword(e.target.value)}
              placeholder="••••••••"
              required
            />
          </div>
          <button
            type="submit"
            disabled={loading}
            className="w-full bg-[#2563EB] hover:bg-[#1D4ED8] text-white font-bold py-2.5 rounded-lg shadow-sm transition-colors flex justify-center items-center"
          >
            {loading ? "AUTHENTICATING..." : "SECURE LOGIN"}
          </button>
        </form>

        <div className="mt-8 text-center text-xs text-[#94A3B8]">
          <p>Demo accounts: rescue_team, safety_manager, admin</p>
          <p>Password for all: Role@2026 (e.g. Safety@2026)</p>
        </div>
      </div>
    </div>
  );
}

// --- LANDING PAGE COMPONENT ---
function LandingPage({ onEnter }) {
  return (
    <div className="min-h-screen bg-[#0F172A] flex flex-col font-sans relative overflow-hidden">
      {/* Background Image with Overlay */}
      <div
        className="absolute inset-0 z-0 bg-cover bg-center bg-no-repeat"
        style={{ backgroundImage: "url('/static/hero-bg.jpg')" }}
      >
        <div className="absolute inset-0 bg-gradient-to-r from-[#0F172A] via-[#0F172A]/80 to-transparent"></div>
        <div className="absolute inset-0 bg-gradient-to-b from-transparent via-[#0F172A]/40 to-[#0F172A]"></div>
      </div>

      {/* Header */}
      <header className="relative z-10 px-8 py-6 flex items-center justify-between">
        <div className="flex items-center gap-3">
          <div className="h-10 w-10 bg-white rounded-lg overflow-hidden shadow-lg border border-[#38BDF8]/30 flex items-center justify-center">
            <img src="/static/logo.png" alt="Logo" className="w-full h-full object-cover" />
          </div>
          <div>
            <div className="font-extrabold text-xl tracking-wider text-white flex items-center gap-1.5">
              OIL-SAFE <span className="text-[#38BDF8]">AI</span>
            </div>
          </div>
        </div>
        <div className="flex items-center gap-4">
          <a href="#" className="text-white hover:text-[#38BDF8] text-sm font-semibold transition">Solutions</a>
          <a href="#" className="text-white hover:text-[#38BDF8] text-sm font-semibold transition">Technology</a>
          <a href="#" className="text-white hover:text-[#38BDF8] text-sm font-semibold transition">About</a>
          <button
            onClick={onEnter}
            className="ml-4 bg-white hover:bg-[#F1F5F9] text-[#0F172A] px-5 py-2 rounded-lg text-sm font-bold shadow-md transition"
          >
            Client Login
          </button>
        </div>
      </header>

      {/* Main Hero Content */}
      <main className="relative z-10 flex-1 flex items-center px-8 sm:px-16 lg:px-24">
        <div className="max-w-3xl space-y-8">
          <div className="inline-flex items-center gap-2 px-3 py-1 rounded-full bg-[#2563EB]/20 border border-[#38BDF8]/30 text-[#38BDF8] text-xs font-bold tracking-widest uppercase font-mono">
            <span className="h-1.5 w-1.5 rounded-full bg-[#38BDF8] animate-pulse"></span>
            Next-Gen Industrial Safety
          </div>

          <h1 className="text-5xl sm:text-6xl lg:text-7xl font-black text-white leading-[1.1] tracking-tight">
            Enterprise AI for <br />
            <span className="text-transparent bg-clip-text bg-gradient-to-r from-[#38BDF8] to-[#2563EB]">
              Oil & Gas Safety
            </span>
          </h1>

          <p className="text-lg text-[#94A3B8] max-w-2xl leading-relaxed">
            Protect your workforce and critical infrastructure with our production-ready decision-support platform.
            Powered by DeBERTa-v3, we instantly extract SIF precursors, detect Life-Saving Rule violations,
            and generate explainable risk scores from raw incident reports.
          </p>

          <div className="flex flex-wrap items-center gap-4 pt-4">
            <button
              onClick={onEnter}
              className="bg-[#2563EB] hover:bg-[#1D4ED8] text-white px-8 py-4 rounded-xl text-lg font-bold shadow-lg transition flex items-center gap-3 group"
            >
              Access Command Center
              <svg className="w-5 h-5 group-hover:translate-x-1 transition-transform" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M14 5l7 7m0 0l-7 7m7-7H3"></path></svg>
            </button>
            <button className="bg-white/10 hover:bg-white/20 text-white backdrop-blur-sm border border-white/20 px-8 py-4 rounded-xl text-lg font-bold transition flex items-center gap-2">
              <span>▶</span> Watch Demo
            </button>
          </div>

          <div className="grid grid-cols-3 gap-6 pt-12 border-t border-white/10">
            <div>
              <div className="text-3xl font-black text-white">94%</div>
              <div className="text-xs text-[#94A3B8] uppercase tracking-wider font-semibold mt-1">AI Accuracy Rate</div>
            </div>
            <div>
              <div className="text-3xl font-black text-white">11</div>
              <div className="text-xs text-[#94A3B8] uppercase tracking-wider font-semibold mt-1">SIF Categories</div>
            </div>
            <div>
              <div className="text-3xl font-black text-white">6</div>
              <div className="text-xs text-[#94A3B8] uppercase tracking-wider font-semibold mt-1">Role Dashboards</div>
            </div>
          </div>
        </div>
      </main>
    </div>
  );
}

// Main OIL-SAFE AI Industrial Safety Platform (Premium White Enterprise Theme)
function App() {
  const [viewMode, setViewMode] = useState("landing"); // landing, auth, app
  const [sidebarCollapsed, setSidebarCollapsed] = useState(false);
  const [isLoggedIn, setIsLoggedIn] = useState(false);
  const [token, setToken] = useState(null);
  const [currentTab, setCurrentTab] = useState("dashboard");
  const [currentUser, setCurrentUser] = useState({
    name: "",
    role: "",
    department: ""
  });
  const [selectedIncidentId, setSelectedIncidentId] = useState(1);
  const [incidentData, setIncidentData] = useState(null);
  const [dashboardData, setDashboardData] = useState(null);
  const [heatmapData, setHeatmapData] = useState([]);
  const [assetsData, setAssetsData] = useState([]);
  const [correctiveActions, setCorrectiveActions] = useState([]);
  const [notifications, setNotifications] = useState([]);
  const [anomaliesData, setAnomaliesData] = useState([]);
  const [forecastData, setForecastData] = useState([]);
  const [loading, setLoading] = useState(true);
  const [searchQuery, setSearchQuery] = useState("");
  const [selectedLocation, setSelectedLocation] = useState(null);
  const [toastMessage, setToastMessage] = useState(null);
  const [criticalBannerAcknowledged, setCriticalBannerAcknowledged] = useState(false);
  const [activePipelineStep, setActivePipelineStep] = useState(9);
  const [analysisTab, setAnalysisTab] = useState("overview");

  const roles = [
    "Safety Manager",
    "Rescue Team",
    "Department Manager",
    "HSE Division",
    "Technician",
    "Admin"
  ];

  // Fetch initial API data
  useEffect(() => {
    if (isLoggedIn) {
      fetchIncidentAnalysis(1);
      fetchDashboard();
      fetchHeatmap();
      fetchAssets();
      fetchCorrectiveActions();
      fetchNotifications();
      fetchAnalytics();
    }
  }, [isLoggedIn]);

  const showToast = (msg) => {
    setToastMessage(msg);
    setTimeout(() => setToastMessage(null), 3000);
  };

  const fetchIncidentAnalysis = async (id) => {
    try {
      setLoading(true);
      const res = await fetch(`/api/incidents/${id}/analyze`);
      if (res.ok) {
        const data = await res.json();
        setIncidentData(data);
      }
    } catch (e) {
      console.error("API error analysis", e);
    } finally {
      setLoading(false);
    }
  };

  const fetchDashboard = async () => {
    try {
      const res = await fetch("/api/dashboard");
      if (res.ok) {
        const data = await res.json();
        setDashboardData(data);
      }
    } catch (e) {
      console.error("API error dashboard", e);
    }
  };

  const fetchHeatmap = async () => {
    try {
      const res = await fetch("/api/risk/heatmap");
      if (res.ok) {
        const data = await res.json();
        setHeatmapData(data);
      }
    } catch (e) {
      console.error("API error heatmap", e);
    }
  };

  const fetchAssets = async () => {
    try {
      const res = await fetch("/api/assets");
      if (res.ok) {
        const data = await res.json();
        setAssetsData(data);
      }
    } catch (e) {
      console.error("API error assets", e);
    }
  };

  const fetchCorrectiveActions = async () => {
    try {
      const res = await fetch("/api/corrective-actions");
      if (res.ok) {
        const data = await res.json();
        setCorrectiveActions(data);
      }
    } catch (e) {
      console.error("API error corrective actions", e);
    }
  };

  const fetchNotifications = async () => {
    try {
      const res = await fetch("/api/notifications");
      if (res.ok) {
        const data = await res.json();
        setNotifications(data);
      }
    } catch (e) {
      console.error("API error notifications", e);
    }
  };

  const fetchAnalytics = async () => {
    try {
      const resAnom = await fetch("/api/analytics/anomalies");
      if (resAnom.ok) setAnomaliesData(await resAnom.json());
      const resFore = await fetch("/api/analytics/forecast");
      if (resFore.ok) setForecastData(await resFore.json());
    } catch (e) {
      console.error("API error analytics", e);
    }
  };

  if (viewMode === "landing") {
    return <LandingPage onEnter={() => setViewMode("auth")} />;
  }

  if (viewMode === "auth" && !isLoggedIn) {
    return <LoginPage onLogin={(userData) => {
      setToken(userData.access_token);
      setCurrentUser({
        name: userData.full_name,
        role: userData.role,
        department: userData.department
      });
      setIsLoggedIn(true);
      setViewMode("app");
    }} />;
  }

  return (
    <div className="flex h-screen overflow-hidden bg-[#F8FAFC] text-[#0F172A] font-sans antialiased">
      {/* Toast Alert */}
      {toastMessage && (
        <div className="fixed bottom-6 right-6 z-50 bg-[#0F172A] text-white px-4 py-3 rounded-lg shadow-2xl flex items-center gap-3 border border-slate-700 animate-bounce">
          <span className="text-[#06B6D4]">⚡</span>
          <span className="font-medium text-xs tracking-wide">{toastMessage}</span>
        </div>
      )}

      {/* 1. SIDEBAR (260px / 72px) */}
      <Sidebar
        collapsed={sidebarCollapsed}
        setCollapsed={setSidebarCollapsed}
        currentTab={currentTab}
        setCurrentTab={setCurrentTab}
      />

      {/* Main Content Area */}
      <div className="flex-1 flex flex-col min-w-0 overflow-hidden bg-[#F8FAFC]">
        {/* 2. TOPBAR */}
        <TopBar
          sidebarCollapsed={sidebarCollapsed}
          setSidebarCollapsed={setSidebarCollapsed}
          currentUser={currentUser}
          setCurrentUser={setCurrentUser}
          roles={roles}
          notifications={notifications}
          searchQuery={searchQuery}
          setSearchQuery={setSearchQuery}
          showToast={showToast}
          onEmergencyClick={() => setCurrentTab("rescue")}
          onHome={() => setCurrentTab("dashboard")}
          onLogout={() => {
            setIsLoggedIn(false);
            setToken(null);
            setViewMode("landing");
          }}
        />

        {/* 3. CRITICAL SAFETY EVENT HERO CARD (Section 7: #FEF2F2 with #FECACA border) */}
        {incidentData && incidentData.risk_score >= 81 && !criticalBannerAcknowledged && (
          <div className="bg-[#FEF2F2] border-y border-[#FECACA] px-6 py-3.5 flex flex-col sm:flex-row sm:items-center justify-between gap-4 shadow-sm pulse-subtle z-10">
            <div className="flex items-center gap-4">
              <div className="h-11 w-11 rounded-lg bg-[#DC2626]/10 border border-[#DC2626]/30 flex items-center justify-center text-[#DC2626] text-2xl font-bold">
                🚨
              </div>
              <div>
                <div className="flex items-center gap-2">
                  <span className="text-[11px] font-black uppercase tracking-widest text-[#DC2626] bg-[#DC2626]/15 px-2 py-0.5 rounded border border-[#DC2626]/30 font-mono">
                    CRITICAL SAFETY EVENT
                  </span>
                  <span className="text-xs font-mono text-[#475569] font-bold">INCIDENT: {incidentData.incident_id}</span>
                  <span className="text-xs font-bold text-[#D97706] uppercase tracking-wider font-mono">• SIF PRECURSOR DETECTED</span>
                </div>
                <div className="text-sm font-bold text-[#0F172A] mt-0.5">
                  {incidentData.location} — <span className="text-[#EA580C]">PRESSURIZED SYSTEM BREACH (250 BAR)</span>
                </div>
              </div>
            </div>

            <div className="flex items-center gap-2.5">
              <div className="text-right hidden md:block mr-2 font-mono">
                <div className="text-[10px] text-[#475569] uppercase font-bold">RISK SCORE</div>
                <div className="text-lg font-black text-[#DC2626]">{incidentData.risk_score} / 100</div>
              </div>
              <button
                onClick={() => setCurrentTab("analysis")}
                className="bg-white hover:bg-slate-50 text-[#2563EB] border border-[#CBD5E1] text-xs font-semibold px-3.5 py-1.5 rounded-lg transition font-mono shadow-sm"
              >
                VIEW INCIDENT
              </button>
              <button
                onClick={() => setCurrentTab("rescue")}
                className="bg-[#DC2626] hover:bg-[#B91C1C] text-white text-xs font-bold px-3.5 py-1.5 rounded-lg transition shadow flex items-center gap-1.5 font-mono"
              >
                <span>🚑</span> RESCUE CENTER
              </button>
              <button
                onClick={() => {
                  setCriticalBannerAcknowledged(true);
                  showToast("Critical Safety Event Acknowledged.");
                }}
                className="text-[#475569] hover:text-[#0F172A] text-xs px-2.5 py-1.5 font-mono transition"
                title="Acknowledge & dismiss banner"
              >
                ACKNOWLEDGE
              </button>
            </div>
          </div>
        )}

        {/* 4. DYNAMIC VIEW CONTENT */}
        <main className="flex-1 overflow-y-auto p-6 space-y-6 bg-[#F8FAFC]">
          {currentTab === "dashboard" && (
            <DashboardView
              data={dashboardData}
              onSelectIncident={(id) => { setSelectedIncidentId(id); fetchIncidentAnalysis(id); setCurrentTab("analysis"); }}
              onOpenRescue={() => setCurrentTab("rescue")}
            />
          )}

          {currentTab === "analysis" && (
            <IncidentAnalysisView
              data={incidentData}
              loading={loading}
              activePipelineStep={activePipelineStep}
              setActivePipelineStep={setActivePipelineStep}
              analysisTab={analysisTab}
              setAnalysisTab={setAnalysisTab}
              onExport={() => window.open(`/api/reports/${incidentData?.db_id || 1}/html`, '_blank')}
              showToast={showToast}
            />
          )}

          {currentTab === "sif" && (
            <SifIntelligenceView data={incidentData} />
          )}

          {currentTab === "copilot" && (
            <SafetyCopilotView incidentData={incidentData} showToast={showToast} />
          )}

          {currentTab === "analytics" && (
            <AnalyticsForecastView anomalies={anomaliesData} forecast={forecastData} />
          )}

          {currentTab === "incidents" && (
            <IncidentsRepositoryView
              onSelectIncident={(id) => { setSelectedIncidentId(id); fetchIncidentAnalysis(id); setCurrentTab("analysis"); }}
              onNewIncident={() => setCurrentTab("new_incident")}
            />
          )}

          {currentTab === "new_incident" && (
            <NewIncidentView
              onSubmitted={(id) => { fetchIncidentAnalysis(id); setCurrentTab("analysis"); showToast("Incident submitted and analyzed by AI pipeline!"); }}
            />
          )}

          {currentTab === "rescue" && (
            <RescueCenterView data={incidentData} showToast={showToast} />
          )}

          {currentTab === "risk_map" && (
            <RefineryRiskHeatmapView
              heatmapData={heatmapData}
              selectedLocation={selectedLocation}
              setSelectedLocation={setSelectedLocation}
            />
          )}

          {currentTab === "assets" && (
            <AssetMonitoringView assets={assetsData} />
          )}

          {currentTab === "corrective_actions" && (
            <CorrectiveActionControlView
              actions={correctiveActions}
              onReload={fetchCorrectiveActions}
              showToast={showToast}
            />
          )}

          {currentTab === "knowledge_base" && (
            <KnowledgeBaseView showToast={showToast} />
          )}

          {currentTab === "alerts" && (
            <AlertsCenterView notifications={notifications} showToast={showToast} />
          )}

          {currentTab === "reports" && (
            <ReportsExportView incidentId={selectedIncidentId} data={incidentData} />
          )}

          {currentTab === "users" && (
            <UsersManagementView currentUser={currentUser} />
          )}

          {currentTab === "settings" && (
            <SystemSettingsView showToast={showToast} />
          )}
        </main>
      </div>
    </div>
  );
}

function Sidebar({ collapsed, setCollapsed, currentTab, setCurrentTab }) {
  const navSections = [
    {
      title: "COMMAND CENTER",
      items: [
        { id: "dashboard", label: "Dashboard", icon: "📊" },
        { id: "copilot", label: "Safety Copilot", icon: "🤖", badge: "AI" }
      ]
    },
    {
      title: "SAFETY INTELLIGENCE",
      items: [
        { id: "incidents", label: "Incidents", icon: "📋" },
        { id: "analysis", label: "AI Analysis", icon: "🔬", badge: "Score 87" },
        { id: "sif", label: "SIF Detection", icon: "⚠️" },
        { id: "analytics", label: "Risk Analytics & Anomaly", icon: "📈" },
        { id: "risk_map", label: "Risk Heatmap", icon: "🗺️" }
      ]
    },
    {
      title: "OPERATIONS",
      items: [
        { id: "rescue", label: "Rescue Center", icon: "🚑", isCritical: true },
        { id: "assets", label: "Assets", icon: "⚙️" },
        { id: "corrective_actions", label: "Corrective Actions", icon: "✅" },
        { id: "alerts", label: "Alerts", icon: "🔔" }
      ]
    },
    {
      title: "KNOWLEDGE",
      items: [
        { id: "knowledge_base", label: "Knowledge Base", icon: "📚" }
      ]
    },
    {
      title: "MANAGEMENT",
      items: [
        { id: "reports", label: "Reports", icon: "📄" },
        { id: "users", label: "Users", icon: "👥" },
        { id: "settings", label: "Settings", icon: "⚙️" }
      ]
    }
  ];

  return (
    <aside className={`transition-all duration-300 bg-[#FFFFFF] border-r border-[#E2E8F0] flex flex-col z-20 shadow-sm ${collapsed ? "w-[72px]" : "w-[260px]"
      }`}>
      {/* Brand Header */}
      <div className="h-16 flex items-center justify-between px-4 border-b border-[#E2E8F0] bg-[#FFFFFF]">
        <div className="flex items-center gap-3 overflow-hidden">
          <div className="h-9 w-9 min-w-[36px] bg-white rounded-lg border border-[#E2E8F0] overflow-hidden shadow-sm flex items-center justify-center">
            <img src="/static/logo.png" alt="Logo" className="w-full h-full object-cover" />
          </div>
          {!collapsed && (
            <div className="truncate">
              <div className="font-extrabold text-sm tracking-wider text-[#0F172A] flex items-center gap-1.5">
                OIL-SAFE <span className="text-[#2563EB]">AI</span>
              </div>
              <div className="text-[9px] uppercase font-mono text-[#475569] tracking-wider truncate font-semibold">
                Industrial Safety AI
              </div>
            </div>
          )}
        </div>
      </div>

      {/* Navigation Links */}
      <div className="flex-1 overflow-y-auto py-3 px-2 space-y-4">
        {navSections.map((section, idx) => (
          <div key={idx} className="space-y-1">
            {!collapsed && (
              <div className="px-3 text-[10px] font-black uppercase tracking-wider text-[#475569] font-mono">
                {section.title}
              </div>
            )}
            {section.items.map((item) => {
              const isActive = currentTab === item.id;
              return (
                <button
                  key={item.id}
                  onClick={() => setCurrentTab(item.id)}
                  title={collapsed ? item.label : ""}
                  className={`w-full flex items-center justify-between px-3 py-2 rounded-lg text-xs font-medium transition text-left group ${isActive
                      ? "bg-[#EFF6FF] text-[#2563EB] border-l-2 border-[#2563EB] font-bold shadow-sm"
                      : item.isCritical
                        ? "text-[#DC2626] hover:bg-[#FEF2F2] font-semibold"
                        : "text-[#475569] hover:bg-[#F1F5F9] hover:text-[#0F172A]"
                    }`}
                >
                  <div className="flex items-center gap-3 truncate">
                    <span className="text-sm">{item.icon}</span>
                    {!collapsed && <span className="truncate">{item.label}</span>}
                  </div>
                  {!collapsed && item.badge && (
                    <span className="text-[10px] font-mono font-bold bg-[#FEF2F2] text-[#DC2626] border border-[#FECACA] px-1.5 py-0.5 rounded">
                      {item.badge}
                    </span>
                  )}
                </button>
              );
            })}
          </div>
        ))}
      </div>

      {/* Footer Status Box */}
      <div className="p-3 border-t border-[#E2E8F0] bg-[#F8FAFC] text-[10px] text-[#475569] font-mono">
        {!collapsed ? (
          <div className="space-y-1">
            <div className="flex items-center justify-between">
              <span>ENGINE:</span>
              <span className="text-[#2563EB] font-bold">DeBERTa-v3</span>
            </div>
            <div className="flex items-center justify-between">
              <span>STATUS:</span>
              <span className="text-[#16A34A] font-bold">● ONLINE</span>
            </div>
          </div>
        ) : (
          <div className="text-center text-[#16A34A] font-bold">●</div>
        )}
      </div>
    </aside>
  );
}

// ----------------- 2. TOPBAR COMPONENT -----------------
function TopBar({ sidebarCollapsed, setSidebarCollapsed, currentUser, setCurrentUser, roles, notifications, searchQuery, setSearchQuery, showToast, onEmergencyClick, onHome, onLogout }) {
  const [showRoleDropdown, setShowRoleDropdown] = useState(false);
  const [showNotifications, setShowNotifications] = useState(false);

  return (
    <header className="h-16 bg-[#FFFFFF] border-b border-[#E2E8F0] px-6 flex items-center justify-between z-10 shadow-sm">
      {/* Left: Collapse Button & Search */}
      <div className="flex items-center gap-4">
        <button
          onClick={() => setSidebarCollapsed(!sidebarCollapsed)}
          className="h-8 w-8 rounded-lg bg-[#F1F5F9] border border-[#E2E8F0] flex items-center justify-center text-[#475569] hover:text-[#2563EB] transition"
          title="Toggle Sidebar"
        >
          ☰
        </button>

        <button
          onClick={onHome}
          className="h-8 px-3 rounded-lg bg-[#F1F5F9] border border-[#E2E8F0] flex items-center justify-center text-[#475569] hover:text-[#2563EB] transition font-bold text-xs"
          title="Back to Home Page"
        >
          🏠 Home
        </button>

        <div className="relative w-80 hidden sm:block">
          <span className="absolute left-3 top-2.5 text-[#94A3B8] text-xs">🔍</span>
          <input
            type="text"
            placeholder="Search incidents, assets, reports..."
            value={searchQuery}
            onChange={(e) => setSearchQuery(e.target.value)}
            className="w-full bg-[#F8FAFC] border border-[#E2E8F0] rounded-lg px-8 py-1.5 text-xs text-[#0F172A] placeholder-[#94A3B8] focus:outline-none focus:border-[#2563EB] font-sans"
          />
        </div>
      </div>

      {/* Center/Right: Live Telemetry Badges */}
      <div className="hidden xl:flex items-center gap-3 text-[11px] font-mono">
        <span className="flex items-center gap-1.5 bg-[#EFF6FF] border border-[#BFDBFE] px-2.5 py-1 rounded-full text-[#2563EB] font-bold">
          <span className="h-1.5 w-1.5 rounded-full bg-[#2563EB] animate-pulse"></span>
          AI ENGINE ONLINE
        </span>
        <span className="flex items-center gap-1.5 bg-[#F0FDF4] border border-[#BBF7D0] px-2.5 py-1 rounded-full text-[#16A34A] font-bold">
          <span className="h-1.5 w-1.5 rounded-full bg-[#16A34A]"></span>
          DATABASE CONNECTED
        </span>
      </div>

      {/* Right: Emergency Indicator, Notifications, User */}
      <div className="flex items-center gap-3">
        {/* Emergency Alert Indicator */}
        <button
          onClick={onEmergencyClick}
          className="h-8 px-2.5 rounded-lg bg-[#FEF2F2] border border-[#FECACA] text-[#DC2626] text-xs font-bold flex items-center gap-1.5 hover:bg-[#FEE2E2] transition font-mono"
        >
          <span className="h-2 w-2 rounded-full bg-[#DC2626] animate-ping"></span>
          <span>CRITICAL: 01</span>
        </button>

        {/* Notifications */}
        <div className="relative">
          <button
            onClick={() => { setShowNotifications(!showNotifications); setShowRoleDropdown(false); }}
            className="h-8 w-8 rounded-lg bg-[#F8FAFC] border border-[#E2E8F0] flex items-center justify-center text-[#475569] hover:text-[#2563EB] relative transition"
          >
            <span>🔔</span>
            {notifications.length > 0 && (
              <span className="absolute -top-1 -right-1 bg-[#DC2626] text-white text-[9px] font-bold h-4 w-4 rounded-full flex items-center justify-center font-mono">
                {notifications.length}
              </span>
            )}
          </button>

          {showNotifications && (
            <div className="absolute right-0 mt-2 w-80 bg-[#FFFFFF] border border-[#CBD5E1] rounded-xl shadow-2xl p-4 z-50">
              <div className="flex items-center justify-between border-b border-[#E2E8F0] pb-2 mb-3">
                <span className="font-bold text-xs text-[#0F172A]">Live System Alerts ({notifications.length})</span>
                <button onClick={() => setShowNotifications(false)} className="text-[#94A3B8] text-xs hover:text-black">✕</button>
              </div>
              <div className="space-y-2 max-h-64 overflow-y-auto">
                {notifications.map((n) => (
                  <div key={n.id} className="p-2.5 rounded-lg bg-[#F8FAFC] border border-[#E2E8F0] text-xs space-y-1">
                    <div className="font-bold text-[#DC2626]">{n.title}</div>
                    <p className="text-[#475569] text-[11px]">{n.message}</p>
                    <div className="text-[10px] text-[#94A3B8] font-mono">{n.created_at || "Just now"}</div>
                  </div>
                ))}
              </div>
            </div>
          )}
        </div>

        {/* User Profile + Role Selector */}
        <div className="relative">
          <button
            onClick={() => { setShowRoleDropdown(!showRoleDropdown); setShowNotifications(false); }}
            className="flex items-center gap-2.5 bg-[#FFFFFF] border border-[#CBD5E1] hover:border-[#2563EB] px-3 py-1.5 rounded-lg transition shadow-sm"
          >
            <div className="h-6 w-6 rounded bg-[#2563EB]/10 border border-[#2563EB] text-[#2563EB] font-bold text-xs flex items-center justify-center font-mono">
              {currentUser.name.charAt(0)}
            </div>
            <div className="text-left hidden md:block">
              <div className="text-xs font-bold text-[#0F172A] leading-none">{currentUser.name}</div>
              <div className="text-[10px] text-[#2563EB] font-mono font-bold leading-tight">{currentUser.role}</div>
            </div>
            <span className="text-[10px] text-[#94A3B8]">▼</span>
          </button>

          {showRoleDropdown && (
            <div className="absolute right-0 mt-2 w-60 bg-[#FFFFFF] border border-[#CBD5E1] rounded-xl shadow-2xl p-2 z-50">
              <div className="text-[10px] font-bold text-[#475569] px-3 py-1.5 uppercase font-mono border-b border-[#E2E8F0] mb-1">
                SWITCH ROLE PERSPECTIVE
              </div>
              {roles.map((r) => (
                <button
                  key={r}
                  onClick={() => {
                    setCurrentUser({ ...currentUser, role: r });
                    setShowRoleDropdown(false);
                    showToast(`Role switched to: ${r}`);
                  }}
                  className={`w-full flex items-center justify-between px-3 py-2 rounded-lg text-xs font-medium text-left transition ${currentUser.role === r ? "bg-[#EFF6FF] text-[#2563EB] border border-[#BFDBFE] font-bold" : "text-[#475569] hover:bg-[#F1F5F9] hover:text-[#0F172A]"
                    }`}
                >
                  <span>{r}</span>
                  {currentUser.role === r && <span className="text-xs font-bold">✓</span>}
                </button>
              ))}
              <div className="border-t border-[#E2E8F0] mt-1 pt-1">
                <button
                  onClick={() => {
                    setShowRoleDropdown(false);
                    if (onLogout) onLogout();
                  }}
                  className="w-full text-left px-3 py-2 text-xs font-bold text-[#DC2626] hover:bg-[#FEF2F2] rounded-lg transition"
                >
                  LOGOUT
                </button>
              </div>
            </div>
          )}
        </div>
      </div>
    </header>
  );
}

// ----------------- 3. COMMAND CENTER DASHBOARD (Section 6) -----------------
function DashboardView({ data, onSelectIncident, onOpenRescue }) {
  if (!data) return <div className="text-[#475569] font-mono text-sm">Loading Command Center Telemetry...</div>;

  const { summary, department_data, risk_trend, severity_distribution, recent_incidents } = data;

  return (
    <div className="space-y-6">
      {/* Top Header & Live System Status */}
      <div className="command-panel p-6 flex flex-col md:flex-row md:items-center justify-between gap-4">
        <div>
          <div className="text-[11px] font-black uppercase tracking-widest text-[#2563EB] font-mono">
            COMMAND CENTER
          </div>
          <h1 className="text-2xl font-black text-[#0F172A] tracking-tight mt-0.5">
            Safety Command Center
          </h1>
          <p className="text-xs text-[#475569] mt-0.5 font-medium">
            Real-time Industrial Safety Intelligence & SIF Precursor Monitoring
          </p>
        </div>

        {/* 4 Status Badges */}
        <div className="grid grid-cols-2 sm:grid-cols-4 gap-2 text-[10px] font-mono">
          <div className="bg-[#F8FAFC] border border-[#E2E8F0] p-2.5 rounded-lg">
            <span className="text-[#475569] block text-[9px] font-bold">SYSTEM STATUS</span>
            <span className="text-[#16A34A] font-bold">● OPERATIONAL</span>
          </div>
          <div className="bg-[#F8FAFC] border border-[#E2E8F0] p-2.5 rounded-lg">
            <span className="text-[#475569] block text-[9px] font-bold">AI ENGINE</span>
            <span className="text-[#2563EB] font-bold">● ONLINE</span>
          </div>
          <div className="bg-[#F8FAFC] border border-[#E2E8F0] p-2.5 rounded-lg">
            <span className="text-[#475569] block text-[9px] font-bold">RAG ENGINE</span>
            <span className="text-[#06B6D4] font-bold">● READY</span>
          </div>
          <div className="bg-[#F8FAFC] border border-[#E2E8F0] p-2.5 rounded-lg">
            <span className="text-[#475569] block text-[9px] font-bold">DATABASE</span>
            <span className="text-[#16A34A] font-bold">● CONNECTED</span>
          </div>
        </div>
      </div>

      {/* 6 KEY METRIC CARDS */}
      <div className="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-6 gap-3">
        <MetricCard title="Total Incidents" value="1,248" trend="↑ 12.4%" icon="📋" trendUp />
        <MetricCard title="Critical Events" value="18" trend="↑ 4 active" icon="🚨" isCritical />
        <MetricCard title="SIF Precursors" value="42" trend="+8.2%" icon="⚠️" isWarning />
        <MetricCard title="Open Actions" value="76" trend="12 OVERDUE" icon="✅" isOverdue />
        <MetricCard title="LSR Violations" value="129" trend="3 this week" icon="🛡️" isWarning />
        <MetricCard title="High-Risk Assets" value="23" trend="Unit-3 T-301" icon="⚙️" isCritical />
      </div>

      {/* Middle Analytics Grid */}
      <div className="grid grid-cols-1 lg:grid-cols-12 gap-6">
        {/* Risk Trend Line Visualization */}
        <div className="lg:col-span-8 command-panel p-6 space-y-4">
          <div className="flex items-center justify-between">
            <div>
              <h3 className="text-xs font-bold uppercase tracking-wider text-[#2563EB] font-mono">
                6-Month Risk & SIF Trend Analytics
              </h3>
              <p className="text-[11px] text-[#475569]">Historical monthly average risk scores across refinery operations</p>
            </div>
            <span className="text-xs font-mono text-[#475569] font-bold">Apr 2024 – Sep 2024</span>
          </div>

          <div className="h-56 flex items-end justify-between gap-3 pt-6 px-2 bg-[#F8FAFC] rounded-lg border border-[#E2E8F0]">
            {risk_trend?.map((item, idx) => (
              <div key={idx} className="flex-1 flex flex-col items-center gap-2 h-full justify-end">
                <div className="text-[11px] font-mono font-bold text-[#2563EB]">{item.avg_risk}</div>
                <div
                  className={`w-full rounded-t transition-all ${item.avg_risk >= 80 ? 'bg-[#DC2626] shadow-sm' : item.avg_risk >= 60 ? 'bg-[#EA580C]' : 'bg-[#2563EB]'
                    }`}
                  style={{ height: `${(item.avg_risk / 100) * 140}px` }}
                ></div>
                <div className="text-[10px] text-[#475569] font-mono text-center truncate w-full font-bold">{item.month}</div>
              </div>
            ))}
          </div>
        </div>

        {/* Severity Distribution */}
        <div className="lg:col-span-4 command-panel p-6 space-y-4">
          <h3 className="text-xs font-bold uppercase tracking-wider text-[#EA580C] font-mono">
            Incident Severity Breakdown
          </h3>
          <div className="space-y-3 pt-2">
            {severity_distribution?.map((s, idx) => (
              <div key={idx} className="space-y-1">
                <div className="flex items-center justify-between text-xs">
                  <span className="font-semibold text-[#0F172A]">{s.name}</span>
                  <span className="font-mono text-[#475569] font-bold">{s.value} incidents</span>
                </div>
                <div className="h-2 bg-[#F1F5F9] rounded-full overflow-hidden">
                  <div className="h-full rounded-full" style={{ width: `${(s.value / 12) * 100}%`, backgroundColor: s.color }}></div>
                </div>
              </div>
            ))}
          </div>
        </div>
      </div>

      {/* Bottom Grid: Department Risks & Recent Incidents */}
      <div className="grid grid-cols-1 lg:grid-cols-12 gap-6">
        {/* Department Compliance Table */}
        <div className="lg:col-span-6 command-panel p-6 space-y-3">
          <h3 className="text-xs font-bold uppercase tracking-wider text-[#0F172A] font-mono">
            Departmental Risk & LOTO Governance
          </h3>
          <div className="overflow-x-auto">
            <table className="w-full text-left text-xs bg-white">
              <thead>
                <tr className="border-b border-[#E2E8F0] text-[#475569] font-mono text-[10px] bg-[#F8FAFC]">
                  <th className="py-2.5 px-3">DEPARTMENT</th>
                  <th className="py-2.5 px-3">RISK</th>
                  <th className="py-2.5 px-3">LOTO COMPLIANCE</th>
                  <th className="py-2.5 px-3">INCIDENTS</th>
                </tr>
              </thead>
              <tbody className="divide-y divide-[#E2E8F0] font-mono">
                {department_data?.map((dept, i) => (
                  <tr key={i} className="hover:bg-[#F8FAFC]">
                    <td className="py-2.5 px-3 font-bold text-[#0F172A] font-sans">{dept.department}</td>
                    <td className="py-2.5 px-3 text-[#DC2626] font-bold">{dept.risk_score}</td>
                    <td className="py-2.5 px-3 text-[#16A34A] font-bold">{dept.loto_compliance}%</td>
                    <td className="py-2.5 px-3 text-[#475569] font-bold">{dept.incidents}</td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </div>

        {/* Recent Critical Incidents */}
        <div className="lg:col-span-6 command-panel p-6 space-y-3">
          <div className="flex items-center justify-between">
            <h3 className="text-xs font-bold uppercase tracking-wider text-[#2563EB] font-mono">
              Recent Safety Telemetry Events
            </h3>
            <span className="text-[10px] text-[#475569] font-mono font-bold">REAL-TIME</span>
          </div>

          <div className="space-y-2">
            {recent_incidents?.map((inc) => (
              <div
                key={inc.id}
                onClick={() => onSelectIncident(inc.id)}
                className="p-3.5 bg-[#F8FAFC] border border-[#E2E8F0] hover:border-[#2563EB] hover:bg-[#F1F5F9] rounded-lg cursor-pointer transition flex items-center justify-between shadow-sm"
              >
                <div>
                  <div className="font-bold text-xs text-[#0F172A]">{inc.title}</div>
                  <div className="text-[11px] text-[#475569] mt-0.5 font-mono">{inc.location} • {inc.date}</div>
                </div>
                <span className="text-xs font-mono font-bold text-[#DC2626] bg-[#FEF2F2] border border-[#FECACA] px-2 py-0.5 rounded">
                  RISK: {inc.risk_score}
                </span>
              </div>
            ))}
          </div>
        </div>
      </div>
    </div>
  );
}

// ----------------- 4. AI INCIDENT INTELLIGENCE VIEW (3-TIER + 11-STAGE PIPELINE) -----------------
function IncidentAnalysisView({ data, loading, activePipelineStep, setActivePipelineStep, analysisTab, setAnalysisTab, onExport, showToast }) {
  if (loading || !data) {
    return (
      <div className="command-panel p-12 text-center text-[#475569] space-y-3">
        <div className="text-3xl animate-spin text-[#2563EB]">⚙️</div>
        <div className="text-xs font-mono tracking-wider font-bold">EXECUTING DeBERTa NLP & SIF PRECURSOR PIPELINE...</div>
      </div>
    );
  }

  const pipelineStages = [
    "INCIDENT REPORT",
    "TEXT PROCESSING",
    "DeBERTa NLP",
    "HAZARD DETECTION",
    "SIF CLASSIFICATION",
    "LSR ANALYSIS",
    "RAG RETRIEVAL",
    "LLM REASONING",
    "RISK ENGINE",
    "SHAP EXPLANATION",
    "SAFETY RECOMMENDATION"
  ];

  const tabs = [
    { id: "overview", label: "Overview" },
    { id: "ai_analysis", label: "AI Analysis" },
    { id: "sif", label: "SIF" },
    { id: "lsr", label: "LSR" },
    { id: "rca", label: "RCA" },
    { id: "evidence", label: "Evidence" },
    { id: "recommendations", label: "Recommendations" },
    { id: "actions", label: "Corrective Actions" },
    { id: "audit", label: "Audit Log" }
  ];

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="command-panel p-6 flex flex-col md:flex-row md:items-center justify-between gap-4">
        <div>
          <div className="text-[10px] font-mono uppercase tracking-widest text-[#2563EB] font-bold">
            AI INCIDENT INTELLIGENCE • {data.incident_id}
          </div>
          <h1 className="text-xl font-black text-[#0F172A] mt-0.5">{data.title}</h1>
          <p className="text-xs text-[#475569] font-mono mt-0.5 font-medium">
            LOCATION: {data.location} | ASSET: {data.asset}
          </p>
        </div>

        <div className="flex items-center gap-3">
          <button
            onClick={onExport}
            className="bg-[#2563EB] hover:bg-[#1D4ED8] text-white text-xs font-bold px-4 py-2 rounded-lg transition font-mono flex items-center gap-2 shadow"
          >
            <span>📄</span> EXPORT HSE REPORT (PDF)
          </button>
        </div>
      </div>

      {/* 9-Tab Incident Navigator */}
      <div className="flex items-center gap-1 border-b border-[#E2E8F0] pb-1 overflow-x-auto font-mono text-xs">
        {tabs.map((tab) => (
          <button
            key={tab.id}
            onClick={() => setAnalysisTab(tab.id)}
            className={`px-3.5 py-1.5 rounded-t-lg font-semibold transition ${analysisTab === tab.id
                ? "bg-white text-[#2563EB] border-t border-x border-[#CBD5E1] font-bold shadow-sm"
                : "text-[#475569] hover:text-[#0F172A]"
              }`}
          >
            {tab.label}
          </button>
        ))}
      </div>

      {/* 10. AI PROCESS VISUALIZATION PIPELINE (11 Technical Nodes) */}
      <div className="command-panel p-4 space-y-2">
        <div className="flex items-center justify-between text-[10px] font-mono text-[#475569]">
          <span className="uppercase text-[#2563EB] font-bold">● AI PROCESSING PIPELINE FLOW</span>
          <span className="font-bold">11 / 11 STAGES EXECUTED</span>
        </div>
        <div className="grid grid-cols-2 sm:grid-cols-4 lg:grid-cols-11 gap-1.5 pt-1">
          {pipelineStages.map((stage, idx) => {
            const isActive = idx <= activePipelineStep;
            return (
              <div
                key={idx}
                onClick={() => setActivePipelineStep(idx)}
                className={`p-2 rounded-lg text-center cursor-pointer transition border text-[9px] font-mono font-bold leading-tight ${idx === activePipelineStep
                    ? "bg-[#EFF6FF] border-[#93C5FD] text-[#2563EB] shadow-sm"
                    : isActive
                      ? "bg-white border-[#CBD5E1] text-[#0F172A]"
                      : "bg-[#F8FAFC] border-[#E2E8F0] text-[#94A3B8]"
                  }`}
              >
                <div className="text-[8px] opacity-70">STAGE {idx + 1}</div>
                <div className="truncate mt-0.5">{stage}</div>
              </div>
            );
          })}
        </div>
      </div>

      {/* 9. THREE-COLUMN / TIER WORKSTATION */}
      <div className="grid grid-cols-1 lg:grid-cols-12 gap-6">
        {/* LEFT COLUMN: INCIDENT DATA (4 COLS) */}
        <div className="lg:col-span-4 space-y-4">
          <div className="command-panel p-5 space-y-3">
            <h3 className="text-xs font-bold uppercase tracking-wider text-[#2563EB] font-mono flex items-center gap-2">
              <span>📋</span> INCIDENT DATA
            </h3>

            <div className="space-y-2.5 text-xs">
              <div className="bg-[#F8FAFC] p-2.5 rounded-lg border border-[#E2E8F0]">
                <span className="text-[#475569] text-[10px] block font-mono font-semibold">PRIMARY ASSET:</span>
                <span className="font-bold text-[#0F172A]">{data.asset}</span>
                <span className="text-[11px] text-[#EA580C] block mt-0.5 font-mono font-bold">Rating: 250 bar / Pressure System</span>
              </div>

              <div className="bg-[#F8FAFC] p-2.5 rounded-lg border border-[#E2E8F0]">
                <span className="text-[#475569] text-[10px] block font-mono font-semibold">PRIMARY HAZARD:</span>
                <span className="font-bold text-[#DC2626]">{data.primary_hazard}</span>
                <span className="text-[11px] text-[#475569] block mt-0.5">Secondary: {data.secondary_hazard}</span>
              </div>

              <div className="bg-[#F8FAFC] p-2.5 rounded-lg border border-[#E2E8F0]">
                <span className="text-[#475569] text-[10px] block font-mono font-semibold">INJURY STATUS:</span>
                <span className="font-bold text-[#EA580C]">Thermal Burn</span>
                <p className="text-[11px] text-[#475569] mt-1">Technician sustained burn injury after fluid ignited against 140°C surface.</p>
              </div>

              <div className="bg-[#F8FAFC] p-2.5 rounded-lg border border-[#E2E8F0]">
                <span className="text-[#475569] text-[10px] block font-mono font-semibold">EQUIPMENT & PPE INTEGRITY:</span>
                <p className="text-[11px] text-[#475569] mt-1 leading-relaxed">
                  Flanged joint had hairline crack. Inadequate pressure isolation. Technician was missing face shield and proper thermal gloves.
                </p>
              </div>
            </div>
          </div>

          {/* SIF PRECURSOR ANALYSIS CARD (Section 12) */}
          <div className="command-panel p-5 border-l-4 border-l-[#DC2626] space-y-3 bg-[#FEF2F2]/30">
            <div className="flex items-center justify-between">
              <span className="text-xs font-bold uppercase tracking-wider text-[#DC2626] font-mono">
                SIF PRECURSOR ANALYSIS
              </span>
              <span className="text-xs font-mono font-bold text-[#DC2626] bg-[#FEF2F2] px-2 py-0.5 rounded border border-[#FECACA]">
                🔴 DETECTED
              </span>
            </div>

            <div className="grid grid-cols-2 gap-2 text-xs font-mono">
              <div className="bg-white p-2 rounded-lg border border-[#E2E8F0]">
                <span className="text-[10px] text-[#475569] block font-bold">CONFIDENCE</span>
                <span className="text-[#2563EB] font-black text-sm">94%</span>
              </div>
              <div className="bg-white p-2 rounded-lg border border-[#E2E8F0]">
                <span className="text-[10px] text-[#475569] block font-bold">PRIMARY CATEGORY</span>
                <span className="text-[#0F172A] font-bold text-xs">{data.sif_category}</span>
              </div>
            </div>

            <div className="text-[11px] font-mono text-[#475569] space-y-1">
              <div className="font-bold">RELATED HAZARDS:</div>
              <div className="flex flex-wrap gap-1 text-[10px]">
                <span className="bg-white px-2 py-0.5 rounded border border-[#E2E8F0] text-[#0F172A] font-bold">Pressure System</span>
                <span className="bg-white px-2 py-0.5 rounded border border-[#E2E8F0] text-[#0F172A] font-bold">Line of Fire</span>
                <span className="bg-white px-2 py-0.5 rounded border border-[#E2E8F0] text-[#0F172A] font-bold">Thermal Hazard</span>
              </div>
            </div>
          </div>
        </div>

        {/* CENTER COLUMN: RISK GAUGE, EXPLAINABLE AI & LSR (5 COLS) */}
        <div className="lg:col-span-5 space-y-4">
          {/* 8. CIRCULAR RISK SCORE VISUALIZATION */}
          <div className="command-panel p-5 flex items-center justify-between">
            <div className="space-y-1">
              <div className="text-[10px] font-mono uppercase tracking-wider text-[#475569] font-bold">RISK SCORE EVALUATION</div>
              <div className="text-2xl font-black text-[#DC2626] font-mono">{data.risk_score} <span className="text-xs text-[#475569]">/ 100</span></div>
              <div className="text-xs font-bold text-[#DC2626] uppercase font-mono tracking-widest">{data.risk_level}</div>
              <p className="text-[11px] text-[#475569] pt-1 font-medium">Industrial High-Energy Hydrocarbon Breach</p>
            </div>

            {/* Circular Gauge Graphic */}
            <div className="relative h-24 w-24 flex items-center justify-center">
              <svg className="w-full h-full transform -rotate-90" viewBox="0 0 36 36">
                <path
                  className="text-[#E2E8F0]"
                  strokeWidth="3.5"
                  stroke="currentColor"
                  fill="none"
                  d="M18 2.0845 a 15.9155 15.9155 0 0 1 0 31.831 a 15.9155 15.9155 0 0 1 0 -31.831"
                />
                <path
                  className="text-[#DC2626]"
                  strokeDasharray="87, 100"
                  strokeWidth="3.5"
                  strokeLinecap="round"
                  stroke="currentColor"
                  fill="none"
                  d="M18 2.0845 a 15.9155 15.9155 0 0 1 0 31.831 a 15.9155 15.9155 0 0 1 0 -31.831"
                />
              </svg>
              <div className="absolute font-mono text-center">
                <span className="text-lg font-black text-[#0F172A]">87</span>
              </div>
            </div>
          </div>

          {/* 11. EXPLAINABLE AI PANEL — WHY IS THIS INCIDENT CRITICAL? */}
          <div className="command-panel p-5 space-y-3">
            <div className="flex items-center justify-between">
              <h3 className="text-xs font-bold uppercase tracking-wider text-[#2563EB] font-mono">
                WHY IS THIS INCIDENT CRITICAL?
              </h3>
              <span className="text-[10px] font-mono text-[#16A34A] font-bold">AI CONFIDENCE: 94%</span>
            </div>

            <div className="space-y-2 font-mono text-xs">
              {data.risk_factors?.map((rf, idx) => {
                const isPositive = rf.contribution > 0;
                return (
                  <div key={idx} className="bg-[#F8FAFC] p-2.5 rounded-lg border border-[#E2E8F0]">
                    <div className="flex items-center justify-between">
                      <span className="text-xs text-[#0F172A] font-sans font-semibold">{rf.factor_name}</span>
                      <span className={`font-bold ${isPositive ? 'text-[#DC2626]' : 'text-[#16A34A]'}`}>
                        {isPositive ? `+${rf.contribution}` : rf.contribution}
                      </span>
                    </div>
                    <div className="text-[10px] text-[#475569] font-sans mt-0.5 italic">
                      "{rf.evidence_snippet}"
                    </div>
                  </div>
                );
              })}
              <div className="border-t border-[#E2E8F0] pt-2 flex items-center justify-between font-bold text-sm">
                <span className="text-[#0F172A]">FINAL RISK SCORE</span>
                <span className="text-[#DC2626]">{data.risk_score}</span>
              </div>
            </div>
          </div>

          {/* 13. LIFE-SAVING RULE (LSR) PANEL */}
          <div className="command-panel p-5 space-y-3">
            <h3 className="text-xs font-bold uppercase tracking-wider text-[#D97706] font-mono">
              LIFE-SAVING RULE (LSR) COMPLIANCE
            </h3>

            <div className="overflow-x-auto">
              <table className="w-full text-left text-xs border-collapse font-sans bg-white">
                <thead>
                  <tr className="border-b border-[#E2E8F0] text-[#475569] text-[10px] font-mono bg-[#F8FAFC]">
                    <th className="py-2 px-2.5">RULE</th>
                    <th className="py-2 px-2.5">STATUS</th>
                    <th className="py-2 px-2.5">SEVERITY</th>
                  </tr>
                </thead>
                <tbody className="divide-y divide-[#E2E8F0] text-xs">
                  {data.lsr_violations?.map((v, i) => (
                    <tr key={i} className="hover:bg-[#F8FAFC]">
                      <td className="py-2 px-2.5 text-[#0F172A] font-medium">{v.rule} {v.name}</td>
                      <td className="py-2 px-2.5 text-[#DC2626] font-bold font-mono">🔴 Violated</td>
                      <td className="py-2 px-2.5 font-mono text-[10px] font-bold text-[#DC2626]">{v.severity}</td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          </div>
        </div>

        {/* RIGHT COLUMN: RCA TREE, HISTORICAL SIMILARITY & RAG EVIDENCE (3 COLS) */}
        <div className="lg:col-span-3 space-y-4">
          {/* 20. ROOT CAUSE VISUALIZATION TREE */}
          <div className="command-panel p-5 space-y-3">
            <h3 className="text-xs font-bold uppercase tracking-wider text-[#0F172A] font-mono">
              ROOT CAUSE ANALYSIS (RCA)
            </h3>

            <div className="space-y-2 text-xs font-mono">
              <div className="p-2.5 bg-[#FEF2F2] border border-[#FECACA] rounded-lg">
                <span className="text-[9px] text-[#DC2626] block font-bold">1. IMMEDIATE CAUSE</span>
                <span className="text-[11px] text-[#0F172A] font-sans font-medium">{data.root_causes?.immediate_cause}</span>
              </div>

              <div className="p-2.5 bg-[#FFFBEB] border border-[#FDE68A] rounded-lg">
                <span className="text-[9px] text-[#D97706] block font-bold">2. CONTRIBUTING FACTORS</span>
                <ul className="list-disc list-inside text-[10px] text-[#475569] font-sans mt-0.5 space-y-0.5">
                  {data.root_causes?.contributing_causes?.map((c, i) => (
                    <li key={i}>{c}</li>
                  ))}
                </ul>
              </div>

              <div className="p-2.5 bg-[#EFF6FF] border border-[#BFDBFE] rounded-lg">
                <span className="text-[9px] text-[#2563EB] block font-bold">3. SYSTEM DEFICIENCIES</span>
                <ul className="list-disc list-inside text-[10px] text-[#475569] font-sans mt-0.5 space-y-0.5">
                  {data.root_causes?.system_causes?.map((s, i) => (
                    <li key={i}>{s}</li>
                  ))}
                </ul>
              </div>
            </div>
          </div>

          {/* 24. HISTORICAL SIMILAR INCIDENTS PANEL */}
          <div className="command-panel p-5 space-y-2 font-mono">
            <div className="flex items-center justify-between text-xs">
              <span className="font-bold text-[#2563EB]">SIMILAR INCIDENTS</span>
              <span className="text-[10px] text-[#475569] font-bold">HISTORICAL</span>
            </div>
            <div className="space-y-1.5 text-xs">
              <div className="bg-[#F8FAFC] p-2 rounded-lg border border-[#E2E8F0] flex justify-between items-center">
                <div>
                  <span className="text-[#2563EB] font-bold block">INC-2023-018</span>
                  <span className="text-[10px] text-[#475569] font-sans">Pressure leak at Unit-2</span>
                </div>
                <span className="text-[11px] font-bold text-[#16A34A]">91% Sim</span>
              </div>
              <div className="bg-[#F8FAFC] p-2 rounded-lg border border-[#E2E8F0] flex justify-between items-center">
                <div>
                  <span className="text-[#2563EB] font-bold block">INC-2022-041</span>
                  <span className="text-[10px] text-[#475569] font-sans">Flange gasket blowout</span>
                </div>
                <span className="text-[11px] font-bold text-[#16A34A]">87% Sim</span>
              </div>
              <div className="bg-[#F8FAFC] p-2 rounded-lg border border-[#E2E8F0] flex justify-between items-center">
                <div>
                  <span className="text-[#2563EB] font-bold block">INC-2021-009</span>
                  <span className="text-[10px] text-[#475569] font-sans">Oil spray hot surface flash</span>
                </div>
                <span className="text-[11px] font-bold text-[#16A34A]">82% Sim</span>
              </div>
            </div>
          </div>

          {/* 22. RAG EVIDENCE VIEW */}
          <div className="command-panel p-5 space-y-3">
            <h3 className="text-xs font-bold uppercase tracking-wider text-[#2563EB] font-mono">
              RAG EVIDENCE RETRIEVAL
            </h3>

            <div className="space-y-2 text-xs">
              {data.retrieved_evidence?.map((doc, idx) => (
                <div key={idx} className="bg-[#F8FAFC] p-2.5 rounded-lg border border-[#E2E8F0] space-y-1 font-mono">
                  <div className="flex items-center justify-between text-[10px]">
                    <span className="text-[#2563EB] font-bold">[Source 0{idx + 1}] {doc.category}</span>
                    <span className="text-[#16A34A] font-bold">{Math.round(doc.score * 100)}% Match</span>
                  </div>
                  <div className="text-[10px] text-[#0F172A] font-sans font-bold">{doc.document_title}</div>
                  <p className="text-[10px] text-[#475569] font-sans italic bg-white p-1.5 rounded border border-[#E2E8F0]">
                    "{doc.content}"
                  </p>
                </div>
              ))}
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}

// ----------------- 5. SIF DETECTION VIEW -----------------
function SifIntelligenceView({ data }) {
  if (!data) return <div className="text-[#475569] font-mono">Loading SIF Precursor Matrix...</div>;

  return (
    <div className="space-y-6">
      <div className="command-panel p-6">
        <div className="text-[10px] font-mono uppercase tracking-widest text-[#2563EB] font-bold">SIF TAXONOMY & PRECURSOR SYSTEM</div>
        <h1 className="text-xl font-bold text-[#0F172A] mt-0.5">Serious Injury & Fatality Precursor Intelligence</h1>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
        <div className="command-panel p-5 border-l-4 border-l-[#DC2626] space-y-2 bg-[#FEF2F2]/20">
          <span className="text-xs font-bold uppercase text-[#DC2626] font-mono">SIF PRECURSOR TRIGGER</span>
          <div className="text-xl font-black text-[#0F172A] font-mono">CRITICAL PRECURSOR DETECTED</div>
          <p className="text-xs text-[#475569]">Energy Isolation failure on pressurized 250 bar hydrocarbon line with ignition source proximity.</p>
        </div>

        <div className="command-panel p-5 border-l-4 border-l-[#2563EB] space-y-2 bg-[#EFF6FF]/30">
          <span className="text-xs font-bold uppercase text-[#2563EB] font-mono">AI INFERENCE CONFIDENCE</span>
          <div className="text-xl font-black text-[#2563EB] font-mono">94.0% CONFIDENCE</div>
          <p className="text-xs text-[#475569]">Calculated by DeBERTa-v3 model across 11 high-energy industrial consequence taxonomies.</p>
        </div>

        <div className="command-panel p-5 border-l-4 border-l-[#EA580C] space-y-2 bg-[#FFF7ED]/30">
          <span className="text-xs font-bold uppercase text-[#EA580C] font-mono">POTENTIAL SEVERITY</span>
          <div className="text-xl font-black text-[#EA580C] font-mono">FATALITY / PERMANENT DISABILITY</div>
          <p className="text-xs text-[#475569]">High potential for acute blast trauma or fatal burn injury in line-of-fire without deluge mitigation.</p>
        </div>
      </div>
    </div>
  );
}

// ----------------- 6. AI SAFETY COPILOT (Section 19: Clean White + Light Blue AI) -----------------
function SafetyCopilotView({ incidentData, showToast }) {
  const [messages, setMessages] = useState([
    {
      sender: "copilot",
      text: "Hello, I am the OIL-SAFE AI Safety Copilot. You can ask me about SIF precursors, root cause analysis, Life-Saving Rules, dynamic risk scoring, or similar historical incidents in our refinery repository."
    }
  ]);
  const [inputQuery, setInputQuery] = useState("");
  const [loading, setLoading] = useState(false);

  const presets = [
    "Why was this incident classified as SIF?",
    "What caused the 87/100 risk score?",
    "Which Life-Saving Rules were violated?",
    "Show similar historical incidents.",
    "What corrective actions are recommended?",
    "What are the recurring hazards in Unit-3?"
  ];

  const handleSend = async (q) => {
    const queryToSend = q || inputQuery;
    if (!queryToSend.trim()) return;

    const userMsg = { sender: "user", text: queryToSend };
    setMessages(prev => [...prev, userMsg]);
    setInputQuery("");
    setLoading(true);

    try {
      const res = await fetch("/api/copilot/query", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ query: queryToSend, incident_id: 1 })
      });
      if (res.ok) {
        const data = await res.json();
        const botMsg = {
          sender: "copilot",
          text: data.answer,
          confidence: data.confidence,
          evidence: data.evidence,
          actions: data.suggested_actions,
          incidentIds: data.related_incident_ids
        };
        setMessages(prev => [...prev, botMsg]);
      }
    } catch (e) {
      console.error(e);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="space-y-6 max-w-4xl">
      <div className="command-panel p-6 flex items-center justify-between">
        <div>
          <div className="text-[10px] font-mono uppercase tracking-widest text-[#2563EB] font-bold">LLM & RAG ASSISTANT</div>
          <h1 className="text-xl font-bold text-[#0F172A] mt-0.5">🤖 Safety Copilot</h1>
        </div>
        <span className="text-xs font-mono text-[#16A34A] font-bold">● RAG CONTEXT LOADED</span>
      </div>

      {/* Preset Pills */}
      <div className="flex flex-wrap gap-2">
        {presets.map((p, idx) => (
          <button
            key={idx}
            onClick={() => handleSend(p)}
            className="bg-white hover:bg-[#EFF6FF] border border-[#E2E8F0] hover:border-[#2563EB] text-[#475569] hover:text-[#2563EB] text-xs px-3 py-1.5 rounded-lg transition font-mono shadow-sm"
          >
            {p}
          </button>
        ))}
      </div>

      {/* Chat Messages */}
      <div className="command-panel p-5 space-y-4 max-h-[500px] overflow-y-auto bg-[#F8FAFC]">
        {messages.map((m, i) => (
          <div key={i} className={`flex ${m.sender === 'user' ? 'justify-end' : 'justify-start'}`}>
            <div className={`max-w-2xl p-4 rounded-xl text-xs leading-relaxed ${m.sender === 'user'
                ? 'bg-[#2563EB] text-white shadow'
                : 'bg-[#EFF6FF] border border-[#BFDBFE] text-[#0F172A] space-y-3 shadow-sm'
              }`}>
              <div className="flex items-center gap-2 font-mono text-[10px] font-bold text-[#2563EB]">
                <span>{m.sender === 'user' ? '👤 SAFETY OPERATOR' : '🤖 SAFETY COPILOT'}</span>
                {m.confidence && <span className="text-[#16A34A]">({Math.round(m.confidence * 100)}% Confidence)</span>}
              </div>
              <p className="font-sans text-xs font-medium">{m.text}</p>

              {/* Retrieved Sources & Suggested Actions */}
              {m.evidence && m.evidence.length > 0 && (
                <div className="pt-2 border-t border-[#BFDBFE] space-y-1.5 font-mono">
                  <div className="text-[10px] text-[#2563EB] font-bold">RETRIEVED RAG EVIDENCE:</div>
                  {m.evidence.map((ev, evIdx) => (
                    <div key={evIdx} className="bg-white p-2 rounded-lg text-[10px] text-[#475569] border border-[#BFDBFE]">
                      <span className="text-[#0F172A] font-bold">[{ev.source}] {ev.category}:</span> "{ev.content}"
                    </div>
                  ))}
                </div>
              )}

              {m.actions && (
                <div className="pt-2 border-t border-[#BFDBFE] font-mono">
                  <div className="text-[10px] text-[#EA580C] font-bold">DIRECTIVE RECOMMENDATIONS:</div>
                  <ul className="list-disc list-inside text-[10px] text-[#475569] font-sans mt-0.5 space-y-0.5">
                    {m.actions.map((act, actIdx) => (
                      <li key={actIdx}>{act}</li>
                    ))}
                  </ul>
                </div>
              )}
            </div>
          </div>
        ))}
        {loading && (
          <div className="text-xs font-mono text-[#2563EB] animate-pulse font-bold">
            🤖 DeBERTa & RAG Knowledge Retrieval in progress...
          </div>
        )}
      </div>

      {/* Input Box */}
      <div className="flex gap-2">
        <input
          type="text"
          placeholder="Ask Copilot about SIF, risk scores, LSRs, SOPs, or historical incidents..."
          value={inputQuery}
          onChange={(e) => setInputQuery(e.target.value)}
          onKeyDown={(e) => e.key === 'Enter' && handleSend()}
          className="flex-1 bg-white border border-[#CBD5E1] rounded-lg px-4 py-2.5 text-xs text-[#0F172A] placeholder-[#94A3B8] focus:outline-none focus:border-[#2563EB] shadow-sm"
        />
        <button
          onClick={() => handleSend()}
          className="bg-[#2563EB] hover:bg-[#1D4ED8] text-white font-mono font-bold text-xs px-6 py-2.5 rounded-lg transition shadow"
        >
          SEND
        </button>
      </div>
    </div>
  );
}

// ----------------- 7. RISK ANALYTICS & ANOMALY DETECTION -----------------
function AnalyticsForecastView({ anomalies, forecast }) {
  return (
    <div className="space-y-6">
      <div className="command-panel p-6">
        <div className="text-[10px] font-mono uppercase tracking-widest text-[#2563EB] font-bold">PREDICTIVE AI & PATTERN RECOGNITION</div>
        <h1 className="text-xl font-bold text-[#0F172A] mt-0.5">Safety Anomaly Detection & 30-Day Risk Forecast</h1>
      </div>

      {/* Anomaly Detection Cards */}
      <div className="space-y-3">
        <div className="text-xs font-bold font-mono text-[#DC2626] uppercase tracking-wider">
          ⚠ ACTIVE ANOMALY DETECTIONS
        </div>
        <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
          {anomalies?.map((anom) => (
            <div key={anom.id} className="command-panel p-5 border-l-4 border-l-[#DC2626] space-y-2">
              <div className="flex items-center justify-between font-mono">
                <span className="text-[10px] text-[#475569] font-bold">{anom.id}</span>
                <span className="text-xs font-bold text-[#DC2626] bg-[#FEF2F2] px-2 py-0.5 rounded border border-[#FECACA]">
                  {anom.deviation} DEVIATION
                </span>
              </div>
              <h4 className="text-sm font-bold text-[#0F172A]">{anom.title}</h4>
              <div className="text-xs text-[#475569] font-mono">{anom.location}</div>
              <div className="bg-[#F8FAFC] p-2 rounded-lg text-[11px] font-mono space-y-1 border border-[#E2E8F0]">
                <div className="flex justify-between"><span>BASELINE:</span><span className="text-[#475569]">{anom.baseline}</span></div>
                <div className="flex justify-between"><span>CURRENT:</span><span className="text-[#DC2626] font-bold">{anom.current}</span></div>
              </div>
              <p className="text-[11px] text-[#475569] pt-1">{anom.details}</p>
            </div>
          ))}
        </div>
      </div>

      {/* 30-Day Risk Forecast Cards */}
      <div className="space-y-3 pt-4">
        <div className="text-xs font-bold font-mono text-[#2563EB] uppercase tracking-wider">
          📈 30-DAY PREDICTIVE SAFETY RISK FORECAST
        </div>
        <div className="grid grid-cols-1 md:grid-cols-4 gap-4 font-mono">
          {forecast?.map((fc, idx) => (
            <div key={idx} className="command-panel p-5 space-y-2">
              <div className="flex items-center justify-between">
                <span className="text-xs font-bold text-[#0F172A]">{fc.zone}</span>
                <span className={`text-[10px] font-bold px-2 py-0.5 rounded ${fc.forecast_30d === 'HIGH' ? 'bg-[#FEF2F2] text-[#DC2626] border border-[#FECACA]' : 'bg-[#EFF6FF] text-[#2563EB] border border-[#BFDBFE]'
                  }`}>
                  {fc.forecast_30d} RISK
                </span>
              </div>
              <div className="text-[10px] text-[#475569]">CONFIDENCE: {Math.round(fc.confidence * 100)}%</div>
              <div className="pt-2 border-t border-[#E2E8F0] text-[10px] space-y-1">
                <div className="text-[#EA580C] font-bold">KEY DRIVER:</div>
                <div className="text-[#475569] font-sans text-xs">{fc.key_risk_driver}</div>
                <div className="text-[#16A34A] font-bold pt-1">PREVENTIVE ACTION:</div>
                <div className="text-[#475569] font-sans text-xs">{fc.recommended_preventive_action}</div>
              </div>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
}

// ----------------- 8. RESCUE CENTER VIEW (Section 16: Clean White + Strong Red) -----------------
function RescueCenterView({ data, showToast }) {
  const workflowSteps = [
    "DETECTED",
    "ALERTED",
    "ISOLATION",
    "RESPONSE",
    "MEDICAL",
    "CONTAINMENT",
    "RESOLVED"
  ];

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="command-panel p-6 border-l-4 border-l-[#DC2626] bg-[#FEF2F2]/40">
        <div className="flex items-center justify-between">
          <div>
            <div className="text-[10px] font-mono uppercase tracking-widest text-[#DC2626] font-bold">
              EMERGENCY RESPONSE OPERATIONS
            </div>
            <h1 className="text-2xl font-black text-[#0F172A] tracking-wide mt-0.5">
              🚨 Emergency Response Center
            </h1>
          </div>
          <span className="bg-[#DC2626] text-white font-mono font-black text-xs px-3 py-1.5 rounded-lg shadow">
            ACTIVE CRITICAL EVENTS: 01
          </span>
        </div>
      </div>

      {/* Emergency Workflow */}
      <div className="command-panel p-4 space-y-2 font-mono">
        <div className="text-[10px] uppercase text-[#475569] font-bold">TACTICAL RESPONSE WORKFLOW</div>
        <div className="flex flex-wrap items-center gap-2 pt-1">
          {workflowSteps.map((step, idx) => (
            <div key={idx} className="flex items-center gap-2">
              <span className={`px-3 py-1 rounded-lg text-xs font-bold ${idx <= 4 ? 'bg-[#FEF2F2] text-[#DC2626] border border-[#FECACA]' : 'bg-[#F8FAFC] text-[#475569] border border-[#E2E8F0]'
                }`}>
                {step}
              </span>
              {idx < workflowSteps.length - 1 && <span className="text-[#CBD5E1] text-xs">→</span>}
            </div>
          ))}
        </div>
      </div>

      {/* Tactical Directives */}
      <div className="grid grid-cols-1 lg:grid-cols-12 gap-6">
        <div className="lg:col-span-8 command-panel p-6 space-y-4">
          <h3 className="text-xs font-bold uppercase tracking-wider text-[#DC2626] font-mono">
            TACTICAL FIRST-RESPONDER DIRECTIVES
          </h3>

          <div className="space-y-2 text-xs">
            {data?.emergency_actions?.map((act, i) => (
              <div key={i} className="p-3 bg-[#F8FAFC] border border-[#E2E8F0] rounded-lg flex items-center justify-between">
                <div className="flex items-center gap-3">
                  <span className="h-5 w-5 rounded bg-[#DC2626] text-white font-mono font-bold text-[10px] flex items-center justify-center">
                    {i + 1}
                  </span>
                  <span className="text-[#0F172A] font-semibold">{act}</span>
                </div>
                <button
                  onClick={() => showToast(`Step ${i + 1} confirmed executed`)}
                  className="bg-white hover:bg-slate-50 text-[#2563EB] border border-[#CBD5E1] text-[10px] font-mono font-bold px-2.5 py-1 rounded-lg transition shadow-sm"
                >
                  EXECUTE
                </button>
              </div>
            ))}
          </div>
        </div>

        <div className="lg:col-span-4 command-panel p-6 space-y-3 font-mono text-xs">
          <h3 className="text-xs font-bold uppercase tracking-wider text-[#2563EB]">
            TELEMETRY & CASUALTY STATUS
          </h3>

          <div className="p-3 bg-[#F8FAFC] rounded-lg border border-[#E2E8F0] space-y-1">
            <span className="text-[#475569] text-[10px] block font-bold">CASUALTY STATUS:</span>
            <span className="text-[#DC2626] font-bold">1 TECHNICIAN (THERMAL BURN)</span>
            <p className="text-[11px] text-[#475569] font-sans">First aid applied; evacuated to site medical stabilization unit.</p>
          </div>

          <div className="p-3 bg-[#F8FAFC] rounded-lg border border-[#E2E8F0] space-y-1">
            <span className="text-[#475569] text-[10px] block font-bold">DELUGE TELEMETRY:</span>
            <span className="text-[#16A34A] font-bold">ACTIVE (1,400 L/MIN FLOW)</span>
          </div>

          <div className="p-3 bg-[#F8FAFC] rounded-lg border border-[#E2E8F0] space-y-1">
            <span className="text-[#475569] text-[10px] block font-bold">PRESSURE BLOWDOWN:</span>
            <span className="text-[#EA580C] font-bold">DEPRESSURIZING (140 BAR REMAINING)</span>
          </div>
        </div>
      </div>
    </div>
  );
}

// ----------------- 9. REFINERY RISK HEATMAP (Section 14) -----------------
function RefineryRiskHeatmapView({ heatmapData, selectedLocation, setSelectedLocation }) {
  return (
    <div className="space-y-6">
      <div className="command-panel p-6 flex items-center justify-between">
        <div>
          <div className="text-[10px] font-mono uppercase tracking-widest text-[#2563EB] font-bold">GEOSPATIAL RISK INTELLIGENCE</div>
          <h1 className="text-xl font-bold text-[#0F172A] mt-0.5">Refinery Risk Heatmap</h1>
        </div>
        <div className="flex items-center gap-3 text-xs font-mono text-[#475569] font-bold">
          <span className="flex items-center gap-1.5"><span className="h-2.5 w-2.5 rounded-full bg-[#DC2626]"></span> 🔴 CRITICAL (≥81)</span>
          <span className="flex items-center gap-1.5"><span className="h-2.5 w-2.5 rounded-full bg-[#EA580C]"></span> 🟠 HIGH (61-80)</span>
          <span className="flex items-center gap-1.5"><span className="h-2.5 w-2.5 rounded-full bg-[#D97706]"></span> 🟡 MEDIUM (41-60)</span>
          <span className="flex items-center gap-1.5"><span className="h-2.5 w-2.5 rounded-full bg-[#16A34A]"></span> 🟢 LOW (&lt;40)</span>
        </div>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-3 lg:grid-cols-4 gap-4">
        {heatmapData?.map((loc) => {
          const isCritical = loc.risk_score >= 81;
          const isHigh = loc.risk_score >= 60 && loc.risk_score < 81;

          return (
            <div
              key={loc.id}
              onClick={() => setSelectedLocation(loc)}
              className={`command-panel p-5 cursor-pointer transition hover:border-[#2563EB] ${isCritical ? 'border-[#DC2626] bg-[#FEF2F2]/30' : ''
                }`}
            >
              <div className="flex items-center justify-between font-mono">
                <span className="text-[10px] text-[#475569] font-bold">{loc.code}</span>
                <span className={`text-xs font-bold px-2 py-0.5 rounded-lg ${isCritical ? 'bg-[#DC2626] text-white' : isHigh ? 'bg-[#EA580C] text-white' : 'bg-[#EFF6FF] text-[#2563EB] border border-[#BFDBFE]'
                  }`}>
                  {loc.risk_score}
                </span>
              </div>
              <h4 className="text-sm font-bold text-[#0F172A] mt-2">{loc.name}</h4>
              <div className="mt-3 pt-2 border-t border-[#E2E8F0] text-[10px] font-mono space-y-1 text-[#475569]">
                <div className="flex justify-between"><span>INCIDENTS:</span><span className="text-[#0F172A] font-bold">{loc.incident_count}</span></div>
                <div className="flex justify-between"><span>SIF EVENTS:</span><span className="text-[#DC2626] font-bold">{loc.sif_count}</span></div>
                <div className="flex justify-between"><span>TOP HAZARD:</span><span className="text-[#EA580C] font-bold truncate max-w-[120px]">{loc.top_hazards?.[0]}</span></div>
              </div>
            </div>
          );
        })}
      </div>

      {selectedLocation && (
        <div className="command-panel p-5 border border-[#2563EB] flex items-center justify-between shadow-sm">
          <div className="text-xs">
            <span className="text-[10px] font-mono text-[#2563EB] font-bold block">SELECTED ZONE INSPECTION</span>
            <span className="text-sm font-bold text-[#0F172A]">{selectedLocation.name}</span>
            <span className="text-xs text-[#475569] ml-3 font-mono">RISK: {selectedLocation.risk_score} | TOP HAZARDS: {selectedLocation.top_hazards?.join(", ")}</span>
          </div>
          <button onClick={() => setSelectedLocation(null)} className="text-[#475569] hover:text-[#0F172A] text-xs font-mono font-bold">✕ CLOSE</button>
        </div>
      )}
    </div>
  );
}

// ----------------- 10. ASSET MONITORING (Section 15) -----------------
function AssetMonitoringView({ assets }) {
  return (
    <div className="space-y-6">
      <div className="command-panel p-6">
        <div className="text-[10px] font-mono uppercase tracking-widest text-[#2563EB] font-bold">EQUIPMENT INTEGRITY</div>
        <h1 className="text-xl font-bold text-[#0F172A] mt-0.5">Asset Risk Intelligence</h1>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
        {assets?.map((a) => (
          <div key={a.id} className="command-panel p-5 space-y-2">
            <div className="flex items-center justify-between font-mono">
              <span className="text-[10px] text-[#475569] font-bold">{a.code}</span>
              <span className={`text-[10px] font-bold px-2 py-0.5 rounded-lg ${a.risk_score >= 80 ? 'bg-[#FEF2F2] text-[#DC2626] border border-[#FECACA]' : 'bg-[#EFF6FF] text-[#2563EB] border border-[#BFDBFE]'
                }`}>
                {a.status}
              </span>
            </div>
            <h4 className="text-sm font-bold text-[#0F172A]">{a.name}</h4>
            <div className="text-xs text-[#475569] font-mono">{a.asset_type} • {a.location}</div>
            <div className="pt-2 border-t border-[#E2E8F0] flex justify-between text-xs font-mono">
              <span className="text-[#475569] font-bold">RISK SCORE:</span>
              <span className="font-bold text-[#DC2626]">{a.risk_score} / 100</span>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
}

// ----------------- 11. CORRECTIVE ACTIONS (Section 17 Kanban) -----------------
function CorrectiveActionControlView({ actions, onReload, showToast }) {
  const columns = ["OPEN", "IN PROGRESS", "UNDER REVIEW", "COMPLETED"];

  return (
    <div className="space-y-6">
      <div className="command-panel p-6 flex items-center justify-between">
        <div>
          <div className="text-[10px] font-mono uppercase tracking-widest text-[#2563EB] font-bold">ACTION GOVERNANCE</div>
          <h1 className="text-xl font-bold text-[#0F172A] mt-0.5">Corrective Action Control</h1>
        </div>
        <div className="flex items-center gap-4 text-xs font-mono">
          <span className="text-[#475569]">TOTAL: <strong>{actions.length}</strong></span>
          <span className="text-[#DC2626] font-bold">12 OVERDUE</span>
        </div>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-4 gap-4">
        {columns.map((col) => {
          const colActions = actions.filter(a => a.status === col || (col === "OPEN" && !a.status));
          return (
            <div key={col} className="command-panel p-5 space-y-3 bg-[#F8FAFC]">
              <div className="flex items-center justify-between border-b border-[#E2E8F0] pb-2">
                <span className="text-xs font-bold font-mono text-[#2563EB]">{col}</span>
                <span className="text-[10px] font-mono text-[#475569] bg-white border border-[#E2E8F0] px-2 py-0.5 rounded-lg font-bold">{colActions.length}</span>
              </div>
              <div className="space-y-2.5">
                {colActions.map((ca) => (
                  <div key={ca.id} className="bg-white p-3.5 rounded-xl border border-[#E2E8F0] text-xs space-y-1.5 shadow-sm">
                    <div className="flex items-center justify-between text-[10px] font-mono">
                      <span className="text-[#2563EB] font-bold">{ca.action_code}</span>
                      <span className="text-[#DC2626] font-bold">{ca.priority}</span>
                    </div>
                    <p className="text-[#0F172A] text-xs leading-snug font-medium">{ca.description}</p>
                    <div className="text-[10px] text-[#475569] font-mono pt-1">OWNER: {ca.owner} • DUE: {ca.due_date}</div>
                  </div>
                ))}
              </div>
            </div>
          );
        })}
      </div>
    </div>
  );
}

// ----------------- 12. INCIDENTS DATA TABLE (Section 18) -----------------
function IncidentsRepositoryView({ onSelectIncident, onNewIncident }) {
  const [incidents, setIncidents] = useState([]);

  useEffect(() => {
    fetch("/api/incidents")
      .then(res => res.json())
      .then(data => setIncidents(data));
  }, []);

  return (
    <div className="space-y-6">
      <div className="command-panel p-6 flex items-center justify-between">
        <div>
          <div className="text-[10px] font-mono uppercase tracking-widest text-[#2563EB] font-bold">INCIDENT REPOSITORY</div>
          <h1 className="text-xl font-bold text-[#0F172A] mt-0.5">Incident Reports & AI Classifications</h1>
        </div>
        <button
          onClick={onNewIncident}
          className="bg-[#2563EB] hover:bg-[#1D4ED8] text-white font-mono font-bold text-xs px-4 py-2 rounded-lg transition flex items-center gap-1.5 shadow"
        >
          <span>➕</span> NEW INCIDENT REPORT
        </button>
      </div>

      <div className="command-panel overflow-x-auto">
        <table className="w-full text-left text-xs border-collapse font-sans bg-white">
          <thead>
            <tr className="border-b border-[#E2E8F0] text-[#475569] text-[10px] font-mono bg-[#F8FAFC]">
              <th className="py-3 px-4">ID</th>
              <th className="py-3 px-4">DATE</th>
              <th className="py-3 px-4">LOCATION</th>
              <th className="py-3 px-4">ASSET</th>
              <th className="py-3 px-4">SEVERITY</th>
              <th className="py-3 px-4">RISK</th>
              <th className="py-3 px-4">SIF</th>
              <th className="py-3 px-4">STATUS</th>
              <th className="py-3 px-4">ACTION</th>
            </tr>
          </thead>
          <tbody className="divide-y divide-[#E2E8F0] font-mono">
            {incidents.map((inc) => (
              <tr key={inc.id} className="hover:bg-[#F8FAFC] transition">
                <td className="py-3 px-4 text-[#2563EB] font-bold">{inc.incident_number}</td>
                <td className="py-3 px-4 text-[#475569]">{inc.date}</td>
                <td className="py-3 px-4 text-[#0F172A] font-sans font-medium">{inc.location}</td>
                <td className="py-3 px-4 text-[#475569] font-sans">{inc.asset}</td>
                <td className="py-3 px-4 text-[#DC2626] font-bold">{inc.severity}</td>
                <td className="py-3 px-4 text-[#DC2626] font-bold">87</td>
                <td className="py-3 px-4 text-[#D97706] font-bold">YES</td>
                <td className="py-3 px-4 text-[#16A34A] font-bold">ACTIVE</td>
                <td className="py-3 px-4">
                  <button
                    onClick={() => onSelectIncident(inc.id)}
                    className="bg-white hover:bg-slate-50 text-[#2563EB] border border-[#CBD5E1] text-[10px] px-3 py-1 rounded-lg font-bold transition shadow-sm"
                  >
                    INSPECT ➔
                  </button>
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
}

// ----------------- 13. NEW INCIDENT FORM (Section 14) -----------------
function NewIncidentView({ onSubmitted }) {
  const [formData, setFormData] = useState({
    title: "Unauthorized Pressurized Flange Repair with Thermal Flash Ignition",
    date: "2024-09-01",
    time: "14:30",
    location: "Refinery Unit-3, Crude Oil Distillation Tower",
    department: "Crude Distillation",
    asset: "Flanged Joint Connection FJ-302",
    report_type: "Unsafe-Act + Unsafe-Condition",
    severity: "HIGH",
    description: "A technician attempted unauthorized repair of a pressurized flanged joint rated at 250 bar without depressurization or supervisor notification. The flanged joint had a hairline crack. Oil sprayed from the damaged connection and ignited after contacting a nearby hot surface at approximately 140°C. The technician suffered a thermal burn. The equipment had deteriorated conditions and inadequate pressure-relief isolation. The technician was working without a face shield and proper gloves. The fire suppression system responded.",
    equipment_condition: "Deteriorated flanged joint connection with active hairline crack and inadequate pressure-relief isolation.",
    ppe_condition: "Technician lacked mandatory full face shield and high-temperature thermal protective gloves.",
    environmental_conditions: "High ambient temperature, adjacent uninsulated piping operated at 140°C.",
    immediate_actions: "Automatic fire deluge system actuated; technician evacuated; unit depressurized to flare."
  });
  const [submitting, setSubmitting] = useState(false);

  const handleSubmit = async (e) => {
    e.preventDefault();
    setSubmitting(true);
    try {
      const res = await fetch("/api/incidents", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(formData)
      });
      if (res.ok) {
        const created = await res.json();
        onSubmitted(created.id);
      }
    } catch (err) {
      console.error(err);
    } finally {
      setSubmitting(false);
    }
  };

  return (
    <div className="space-y-6 max-w-4xl">
      <div className="command-panel p-6">
        <div className="text-[10px] font-mono uppercase tracking-widest text-[#2563EB] font-bold">INCIDENT INTAKE</div>
        <h1 className="text-xl font-bold text-[#0F172A] mt-0.5">Submit Incident for AI Pipeline Analysis</h1>
      </div>

      <form onSubmit={handleSubmit} className="command-panel p-6 space-y-4 text-xs">
        <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
          <div>
            <label className="text-[#475569] font-mono font-bold block mb-1">INCIDENT TITLE:</label>
            <input
              type="text"
              value={formData.title}
              onChange={(e) => setFormData({ ...formData, title: e.target.value })}
              className="w-full bg-[#F8FAFC] border border-[#CBD5E1] rounded-lg p-2 text-[#0F172A] focus:outline-none focus:border-[#2563EB]"
              required
            />
          </div>
          <div>
            <label className="text-[#475569] font-mono font-bold block mb-1">LOCATION:</label>
            <input
              type="text"
              value={formData.location}
              onChange={(e) => setFormData({ ...formData, location: e.target.value })}
              className="w-full bg-[#F8FAFC] border border-[#CBD5E1] rounded-lg p-2 text-[#0F172A] focus:outline-none focus:border-[#2563EB]"
              required
            />
          </div>
          <div>
            <label className="text-[#475569] font-mono font-bold block mb-1">DEPARTMENT:</label>
            <input
              type="text"
              value={formData.department}
              onChange={(e) => setFormData({ ...formData, department: e.target.value })}
              className="w-full bg-[#F8FAFC] border border-[#CBD5E1] rounded-lg p-2 text-[#0F172A] focus:outline-none focus:border-[#2563EB]"
              required
            />
          </div>
          <div>
            <label className="text-[#475569] font-mono font-bold block mb-1">ASSET (RATED PRESSURE / SPEC):</label>
            <input
              type="text"
              value={formData.asset}
              onChange={(e) => setFormData({ ...formData, asset: e.target.value })}
              className="w-full bg-[#F8FAFC] border border-[#CBD5E1] rounded-lg p-2 text-[#0F172A] focus:outline-none focus:border-[#2563EB]"
              required
            />
          </div>
        </div>

        <div>
          <label className="text-[#475569] font-mono font-bold block mb-1">INCIDENT NARRATIVE (RAW TEXT):</label>
          <textarea
            rows="5"
            value={formData.description}
            onChange={(e) => setFormData({ ...formData, description: e.target.value })}
            className="w-full bg-[#F8FAFC] border border-[#CBD5E1] rounded-lg p-2.5 text-[#0F172A] focus:outline-none focus:border-[#2563EB] font-mono text-xs leading-relaxed"
            required
          ></textarea>
        </div>

        <button
          type="submit"
          disabled={submitting}
          className="w-full bg-[#2563EB] hover:bg-[#1D4ED8] text-white font-mono font-bold text-xs py-3 rounded-lg transition shadow uppercase tracking-wider"
        >
          {submitting ? "EXECUTING TRANSFORMER PIPELINE..." : "EXECUTE DeBERTa NLP & SIF PRECURSOR ANALYSIS"}
        </button>
      </form>
    </div>
  );
}

// ----------------- 14. KNOWLEDGE BASE -----------------
function KnowledgeBaseView({ showToast }) {
  const [query, setQuery] = useState("");
  const [results, setResults] = useState([]);
  const [loading, setLoading] = useState(false);

  const handleSearch = async () => {
    if (!query) return;
    setLoading(true);
    try {
      const res = await fetch("/api/rag/query", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ query, top_k: 5 })
      });
      if (res.ok) {
        const data = await res.json();
        setResults(data.results);
      }
    } catch (e) {
      console.error(e);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="space-y-6">
      <div className="command-panel p-6 space-y-3">
        <div className="text-[10px] font-mono uppercase tracking-widest text-[#2563EB] font-bold">RAG VECTOR ENGINE</div>
        <h1 className="text-xl font-bold text-[#0F172A]">Safety Knowledge Intelligence</h1>
        <p className="text-xs text-[#475569]">Query corporate refinery SOPs, LOTO procedures, Life-Saving Rules, and SIF precursor criteria.</p>

        <div className="flex gap-3 pt-2">
          <input
            type="text"
            placeholder="Search e.g. '250 bar pressure isolation', 'LSR #1', 'thermal flash burn'..."
            value={query}
            onChange={(e) => setQuery(e.target.value)}
            className="flex-1 bg-[#F8FAFC] text-xs rounded-lg px-4 py-2 border border-[#CBD5E1] text-[#0F172A] focus:outline-none focus:border-[#2563EB] font-sans"
          />
          <button
            onClick={handleSearch}
            className="bg-[#2563EB] hover:bg-[#1D4ED8] text-white text-xs font-mono font-bold px-5 py-2 rounded-lg transition shadow-sm"
          >
            {loading ? "SEARCHING..." : "SEARCH RAG"}
          </button>
        </div>
      </div>

      {results.length > 0 && (
        <div className="space-y-3">
          {results.map((r, i) => (
            <div key={i} className="command-panel p-5 space-y-1 text-xs">
              <div className="flex items-center justify-between font-mono">
                <span className="font-bold text-[#2563EB]">{r.document_title}</span>
                <span className="text-[#16A34A] text-[10px] font-bold">{Math.round(r.score * 100)}% MATCH</span>
              </div>
              <div className="text-[10px] text-[#475569] font-mono">{r.source} • {r.category}</div>
              <p className="text-[#0F172A] text-xs mt-1 bg-[#F8FAFC] p-2.5 rounded-lg border border-[#E2E8F0] italic">
                "{r.content}"
              </p>
            </div>
          ))}
        </div>
      )}
    </div>
  );
}

// ----------------- 15. ALERTS VIEW -----------------
function AlertsCenterView({ notifications }) {
  return (
    <div className="space-y-6">
      <div className="command-panel p-6">
        <div className="text-[10px] font-mono uppercase tracking-widest text-[#2563EB] font-bold">ALERT DISPATCH CENTER</div>
        <h1 className="text-xl font-bold text-[#0F172A] mt-0.5">Automated Notifications & Emergency Logs</h1>
      </div>

      <div className="space-y-3">
        {notifications?.map((n) => (
          <div key={n.id} className="command-panel p-5 flex items-start gap-4 text-xs">
            <span className="text-2xl">🚨</span>
            <div className="flex-1 space-y-1">
              <div className="flex items-center justify-between font-mono">
                <span className="font-bold text-[#0F172A]">{n.title}</span>
                <span className="text-[10px] bg-[#FEF2F2] text-[#DC2626] border border-[#FECACA] px-2 py-0.5 rounded-lg font-bold">
                  {n.priority}
                </span>
              </div>
              <p className="text-[#475569] text-xs font-sans">{n.message}</p>
              <div className="text-[10px] text-[#475569] font-mono">RECIPIENT: {n.recipient_role} • CHANNEL: {n.channel}</div>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
}

// ----------------- 16. REPORTS EXPORT VIEW -----------------
function ReportsExportView({ incidentId, data }) {
  return (
    <div className="space-y-6 max-w-xl">
      <div className="command-panel p-6">
        <div className="text-[10px] font-mono uppercase tracking-widest text-[#2563EB] font-bold">FORMAL HSE REPORT</div>
        <h1 className="text-xl font-bold text-[#0F172A] mt-0.5">Incident Safety Report Generator</h1>
      </div>

      <div className="command-panel p-6 space-y-4 text-xs">
        <div className="font-mono text-[#2563EB] font-bold">REPORT: {data?.incident_id || "INC-2024-0901-001"}</div>
        <p className="text-[#475569] font-medium">{data?.title}</p>

        <div className="flex flex-col sm:flex-row gap-3 pt-2 font-mono">
          <a
            href={`/api/reports/${data?.db_id || 1}/html`}
            target="_blank"
            className="flex-1 text-center bg-[#EFF6FF] text-[#2563EB] border border-[#BFDBFE] hover:bg-[#DBEAFE] text-xs font-bold px-4 py-2.5 rounded-lg transition shadow-sm"
          >
            PRINTABLE HTML REPORT
          </a>
          <a
            href={`/api/reports/${data?.db_id || 1}/pdf`}
            target="_blank"
            className="flex-1 text-center bg-[#DC2626] text-white hover:bg-[#B91C1C] text-xs font-bold px-4 py-2.5 rounded-lg transition shadow"
          >
            DOWNLOAD PDF
          </a>
        </div>
      </div>
    </div>
  );
}

// ----------------- 17. USERS & ROLES VIEW -----------------
function UsersManagementView({ currentUser }) {
  return (
    <div className="space-y-6 max-w-2xl">
      <div className="command-panel p-6">
        <div className="text-[10px] font-mono uppercase tracking-widest text-[#2563EB] font-bold">ACCESS CONTROL</div>
        <h1 className="text-xl font-bold text-[#0F172A] mt-0.5">Role-Based Access Control (RBAC)</h1>
      </div>

      <div className="command-panel p-6 space-y-3 text-xs">
        <div className="flex justify-between border-b border-[#E2E8F0] pb-2 font-mono">
          <span className="text-[#475569]">CURRENT USER:</span>
          <span className="text-[#0F172A] font-bold">{currentUser.name}</span>
        </div>
        <div className="flex justify-between border-b border-[#E2E8F0] pb-2 font-mono">
          <span className="text-[#475569]">ACTIVE ROLE:</span>
          <span className="text-[#2563EB] font-bold">{currentUser.role}</span>
        </div>
        <div className="flex justify-between font-mono">
          <span className="text-[#475569]">DEPARTMENT:</span>
          <span className="text-[#0F172A] font-bold">{currentUser.department}</span>
        </div>
      </div>
    </div>
  );
}

// ----------------- 18. SYSTEM SETTINGS VIEW -----------------
function SystemSettingsView({ showToast }) {
  return (
    <div className="space-y-6 max-w-3xl">
      <div className="command-panel p-6">
        <div className="text-[10px] font-mono uppercase tracking-widest text-[#2563EB] font-bold">PLATFORM CONFIGURATION</div>
        <h1 className="text-xl font-bold text-[#0F172A] mt-0.5">System & AI Threshold Settings</h1>
      </div>

      <div className="command-panel p-6 space-y-3 text-xs font-mono">
        <div className="flex items-center justify-between p-3.5 bg-[#F8FAFC] rounded-lg border border-[#E2E8F0]">
          <div>
            <div className="text-[#0F172A] font-bold">CRITICAL RISK SCORE THRESHOLD</div>
            <div className="text-[#475569] text-[10px]">Triggers Rescue Team command banner</div>
          </div>
          <span className="text-[#DC2626] font-bold text-sm">81 / 100</span>
        </div>

        <div className="flex items-center justify-between p-3.5 bg-[#F8FAFC] rounded-lg border border-[#E2E8F0]">
          <div>
            <div className="text-[#0F172A] font-bold">SIF CONFIDENCE CUTOFF</div>
            <div className="text-[#475569] text-[10px]">Threshold for SIF Precursor decision</div>
          </div>
          <span className="text-[#2563EB] font-bold text-sm">85%</span>
        </div>

        <button
          onClick={() => showToast("System configuration saved.")}
          className="bg-[#2563EB] hover:bg-[#1D4ED8] text-white font-bold text-xs px-5 py-2.5 rounded-lg transition uppercase shadow"
        >
          SAVE SETTINGS
        </button>
      </div>
    </div>
  );
}

// ----------------- UTILITY CARD COMPONENT (Section 6 & 22) -----------------
function MetricCard({ title, value, trend, icon, isCritical, isWarning, isOverdue, trendUp }) {
  return (
    <div className={`command-panel p-5 space-y-1 font-mono transition ${isCritical ? 'border-l-4 border-l-[#DC2626] bg-[#FEF2F2]/20' : isWarning ? 'border-l-4 border-l-[#EA580C] bg-[#FFF7ED]/20' : isOverdue ? 'border-l-4 border-l-[#D97706] bg-[#FFFBEB]/20' : ''
      }`}>
      <div className="flex items-center justify-between text-[10px] text-[#475569] font-bold">
        <span className="truncate">{title}</span>
        <span className="text-xs">{icon}</span>
      </div>
      <div className="text-2xl font-black text-[#0F172A] tracking-tight">{value}</div>
      <div className={`text-[10px] font-bold ${isCritical ? 'text-[#DC2626]' : isWarning ? 'text-[#EA580C]' : isOverdue ? 'text-[#D97706]' : trendUp ? 'text-[#16A34A]' : 'text-[#475569]'
        }`}>
        {trend}
      </div>
    </div>
  );
}

// Mount App
const root = ReactDOM.createRoot(document.getElementById("root"));
root.render(<App />);
