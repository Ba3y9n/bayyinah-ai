import React, { useState } from 'react';
import { Navbar, NavTab } from './components/Navbar';
import { Footer } from './components/Footer';
import { HomePage } from './pages/HomePage';
import { VerificationPage } from './pages/VerificationPage';
import { ResultPage } from './pages/ResultPage';
import { SourcesPage } from './pages/SourcesPage';
import { HowItWorksPage } from './pages/HowItWorksPage';
import { AboutPage } from './pages/AboutPage';
import { EvaluationPage } from './pages/EvaluationPage';
import { JudgeDemoPage } from './pages/JudgeDemoPage';
import { VerificationResponse } from './types';
import { api } from './services/api';

export function App() {
  const [activeTab, setActiveTab] = useState<NavTab>('home');
  const [currentVerificationResult, setCurrentVerificationResult] = useState<VerificationResponse | null>(null);
  
  // Verification execution state
  const [verifyingText, setVerifyingText] = useState<string | undefined>();
  const [verifyingImage, setVerifyingImage] = useState<string | undefined>();
  const [isDemoVerification, setIsDemoVerification] = useState<boolean>(false);
  const [activeDemoId, setActiveDemoId] = useState<string | undefined>();
  const [verificationError, setVerificationError] = useState<string | null>(null);

  const startVerification = async (
    text?: string, 
    imageBase64?: string, 
    isDemo: boolean = false, 
    demoId?: string
  ) => {
    setVerifyingText(text);
    setVerifyingImage(imageBase64);
    setIsDemoVerification(isDemo);
    setActiveDemoId(demoId);
    setCurrentVerificationResult(null);
    setVerificationError(null);
    setActiveTab('verify');

    try {
      let result: VerificationResponse;
      if (isDemo && demoId) {
        result = await api.verifyDemoCase(demoId);
      } else {
        result = await api.verifyContent({
          text,
          image_base64: imageBase64
        });
      }
      setCurrentVerificationResult(result);
    } catch (err: any) {
      console.error('Verification error:', err);
      setVerificationError(err.message || 'حدث خطأ أثناء فحص المحتوى');
    }
  };

  const handleVerificationComplete = (result: VerificationResponse) => {
    setCurrentVerificationResult(result);
  };

  const handleNewVerification = () => {
    setCurrentVerificationResult(null);
    setVerifyingText(undefined);
    setVerifyingImage(undefined);
    setVerificationError(null);
    setActiveTab('home');
  };

  return (
    <div className="min-h-screen flex flex-col bg-[#F8F9FE] text-bayyinah-navy selection:bg-bayyinah-purple-light selection:text-bayyinah-purple font-sans" dir="rtl">
      {/* Global Navbar */}
      <Navbar activeTab={activeTab} setActiveTab={setActiveTab} />

      {/* Main Page Routing */}
      <main className="flex-1">
        {activeTab === 'home' && (
          <HomePage
            onStartVerification={startVerification}
            onSelectResult={(res) => {
              setCurrentVerificationResult(res);
              setActiveTab('verify');
            }}
            setActiveTab={setActiveTab}
          />
        )}

        {activeTab === 'verify' && (
          <>
            {currentVerificationResult ? (
              <ResultPage
                result={currentVerificationResult}
                onNewVerification={handleNewVerification}
              />
            ) : (
              <VerificationPage
                inputText={verifyingText}
                imageBase64={verifyingImage}
                isDemo={isDemoVerification}
                demoId={activeDemoId}
                result={currentVerificationResult}
                error={verificationError}
                onVerificationComplete={handleVerificationComplete}
                onCancel={handleNewVerification}
              />
            )}
          </>
        )}

        {activeTab === 'sources' && <SourcesPage />}
        {activeTab === 'how-it-works' && <HowItWorksPage />}
        {activeTab === 'evaluation' && <EvaluationPage />}
        {activeTab === 'demo' && <JudgeDemoPage onStartVerification={startVerification} />}
        {activeTab === 'about' && <AboutPage />}
      </main>

      {/* Global Footer */}
      <Footer setActiveTab={setActiveTab} />
    </div>
  );
}

export default App;
