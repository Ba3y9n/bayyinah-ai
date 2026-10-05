import React, { useState } from 'react';
import { Navbar, NavTab } from './components/Navbar';
import { Footer } from './components/Footer';
import { HomePage } from './pages/HomePage';
import { VerificationPage } from './pages/VerificationPage';
import { ResultPage } from './pages/ResultPage';
import { JudgeDemoPage } from './pages/JudgeDemoPage';
import { SourcesPage } from './pages/SourcesPage';
import { KnowledgeBasePage } from './pages/KnowledgeBasePage';
import { SystemHealthPage } from './pages/SystemHealthPage';
import { HelpPage } from './pages/HelpPage';
import { VerificationResponse } from './types';
import { api } from './services/api';

export function App() {
  const [activeTab, setActiveTab] = useState<NavTab>('home');
  const [currentVerificationResult, setCurrentVerificationResult] = useState<VerificationResponse | null>(null);
  
  // Verification execution state
  const [verifyingText, setVerifyingText] = useState<string | undefined>();
  const [verifyingImage, setVerifyingImage] = useState<string | undefined>();
  const [verifyingUrl, setVerifyingUrl] = useState<string | undefined>();
  const [isDemoVerification, setIsDemoVerification] = useState<boolean>(false);
  const [activeDemoId, setActiveDemoId] = useState<string | undefined>();
  const [verificationError, setVerificationError] = useState<string | null>(null);

  const startVerification = async (
    text?: string, 
    imageBase64?: string, 
    isDemo: boolean = false, 
    demoId?: string,
    urlInput?: string,
    mediaFile?: File,
    mediaType?: 'image' | 'video'
  ) => {
    setVerifyingText(text);
    setVerifyingImage(imageBase64);
    setVerifyingUrl(urlInput);
    setIsDemoVerification(isDemo);
    setActiveDemoId(demoId);
    setCurrentVerificationResult(null);
    setVerificationError(null);
    setActiveTab('verify');

    try {
      let result: VerificationResponse;
      if (urlInput) {
        result = await api.verifyUrl(urlInput);
      } else if (mediaFile) {
        if (mediaType === 'video') {
          result = await api.verifyVideo(mediaFile);
        } else {
          result = await api.verifyImage(mediaFile);
        }
      } else if (isDemo && demoId) {
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
    setVerifyingUrl(undefined);
    setVerificationError(null);
    setActiveTab('verify');
  };

  return (
    <div className="min-h-screen flex flex-col bg-bayyinah-ivory text-gray-900 selection:bg-bayyinah-emerald-light selection:text-white font-sans" dir="rtl">
      {/* Global Navbar */}
      <Navbar activeTab={activeTab} setActiveTab={setActiveTab} />

      {/* Main Page Routing */}
      <main className="flex-1 flex flex-col pt-16">
        {activeTab === 'home' && (
          <HomePage
            onStartVerification={() => setActiveTab('verify')}
            setActiveTab={setActiveTab}
          />
        )}

        {activeTab === 'verify' && (
          <>
            {currentVerificationResult ? (
              <ResultPage
                result={currentVerificationResult}
                onNewVerification={handleNewVerification}
                onOpenHelp={() => setActiveTab('health')}
              />
            ) : (
              <VerificationPage
                inputText={verifyingText}
                imageBase64={verifyingImage}
                urlInput={verifyingUrl}
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

        {activeTab === 'judge-demo' && (
          <JudgeDemoPage
            onStartVerification={(text, imageBase64, isDemo, demoId) => {
              startVerification(text, imageBase64, isDemo, demoId);
            }}
          />
        )}

        {activeTab === 'sources' && <SourcesPage />}
        {activeTab === 'knowledge-domains' && <KnowledgeBasePage />}
        {activeTab === 'health' && <SystemHealthPage />}
      </main>

      {/* Global Footer */}
      <Footer setActiveTab={setActiveTab} />
    </div>
  );
}

export default App;

