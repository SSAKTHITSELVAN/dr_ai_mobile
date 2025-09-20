

// // // src/App.js
// // import React, { useState } from 'react';
// // import { Phone, Send, CheckCircle } from 'lucide-react';
// // import './App.css';

// // function App() {
// //   const [phoneNumber, setPhoneNumber] = useState('');
// //   const [isLoading, setIsLoading] = useState(false);
// //   const [showSuccess, setShowSuccess] = useState(false);

// //   const handleSubmit = async (e) => {
// //     e.preventDefault();
// //     if (!phoneNumber.trim()) return;
    
// //     setIsLoading(true);
    
// //     // Submit to Google Forms
// //     const formData = new FormData();
// //     formData.append('entry.1658933364', phoneNumber);
    
// //     try {
// //       await fetch('https://docs.google.com/forms/u/0/d/e/1FAIpQLSfGsdHitQ5v18ZnCcLMZ3WvTc_GAoZKXkJCFVHbI70ph2J0kQ/formResponse', {
// //         method: 'POST',
// //         mode: 'no-cors',
// //         body: formData
// //       });
// //     } catch (error) {
// //       console.error('Failed to submit:', error);
// //     }
    
// //     setIsLoading(false);
// //     setShowSuccess(true);
// //     setPhoneNumber('');
// //   };

// //   return (
// //     <div className="app-container">
// //       {/* Floating Background Elements */}
// //       <div className="floating-elements">
// //         <div className="floating-circle circle-1"></div>
// //         <div className="floating-circle circle-2"></div>
// //         <div className="floating-circle circle-3"></div>
// //       </div>

// //       <div className="content-wrapper">
// //         {/* Header with Logo */}
// //         <header className="header">
// //           <img 
// //             src="https://image2url.com/images/1758185046787-549ef537-216c-408a-91b0-51d04dec902f.png" 
// //             alt="Bizzap Logo" 
// //             className="logo-image"
// //           />
// //           <h1 className="logo">bizzap</h1>
// //           <p className="tagline">Turn your sourcing from static to social</p>
// //         </header>

// //         {/* Main Content */}
// //         <main className="main-content">
// //           {/* Hero Section */}
// //           <div className="hero-section">
// //             <h2 className="hero-title">
// //               Post requirements<br />
// //               Find leads<br />
// //               Connect with business
// //             </h2>
// //             <div className="hero-subtitle">
// //               Join the waitlist and get 3 months premium subscription for free
// //             </div>
// //           </div>
          
// //           {/* Premium Features */}
// //           <div className="premium-badge">
// //             <h3 className="premium-title">Bizzap Premium (Free)</h3>
// //             <ul className="premium-features">
// //               <li>Get free leads</li>
// //               <li>Company Verified Badge</li>
// //               <li>Product Catalogue (up-to 10)</li>
// //               <li>AI Business Assistant</li>
// //               <li>Referral leader board</li>
// //             </ul>
// //           </div>

// //           {/* Phone Form */}
// //           <div className="waitlist-form">
// //             {!showSuccess ? (
// //               <form onSubmit={handleSubmit}>
// //                 <div className="form-group">
// //                   <div className="input-wrapper">
// //                     <Phone className="input-icon" />
// //                     <input
// //                       type="tel"
// //                       value={phoneNumber}
// //                       onChange={(e) => setPhoneNumber(e.target.value)}
// //                       placeholder="Enter your phone number"
// //                       className="form-input"
// //                       required
// //                     />
// //                   </div>
// //                 </div>
// //                 <button 
// //                   type="submit" 
// //                   className="join-button"
// //                   disabled={isLoading || !phoneNumber.trim()}
// //                 >
// //                   {isLoading ? (
// //                     <div className="loading-content">
// //                       <div className="spinner"></div>
// //                       <span>Processing...</span>
// //                     </div>
// //                   ) : (
// //                     <div className="button-content">
// //                       <Send className="button-icon" />
// //                       <span>Join Waitlist - FREE Premium</span>
// //                     </div>
// //                   )}
// //                 </button>
// //               </form>
// //             ) : (
// //               <div className="success-message">
// //                 <CheckCircle className="success-icon" />
// //                 <div className="success-text">
// //                   <strong>Welcome aboard!</strong><br />
// //                   You're now on the waitlist. We'll notify you when Bizzap launches!
// //                 </div>
// //               </div>
// //             )}
// //           </div>
// //         </main>

// //         {/* Footer */}
// //         <footer className="footer">
// //           © 2025 Bizzap. All rights reserved.
// //         </footer>
// //       </div>
// //     </div>
// //   );
// // }

// // export default App;


// // src/App.js
// import React, { useState } from 'react';
// import { Phone, Send, CheckCircle } from 'lucide-react';
// import './App.css';

// function App() {
//   const [phoneNumber, setPhoneNumber] = useState('');
//   const [isLoading, setIsLoading] = useState(false);
//   const [showSuccess, setShowSuccess] = useState(false);

//   const handleSubmit = async (e) => {
//     e.preventDefault();
//     if (!phoneNumber.trim()) return;
    
//     setIsLoading(true);
    
//     // Submit to Google Forms
//     const formData = new FormData();
//     formData.append('entry.1658933364', phoneNumber);
    
//     try {
//       await fetch('https://docs.google.com/forms/u/0/d/e/1FAIpQLSfGsdHitQ5v18ZnCcLMZ3WvTc_GAoZKXkJCFVHbI70ph2J0kQ/formResponse', {
//         method: 'POST',
//         mode: 'no-cors',
//         body: formData
//       });
//     } catch (error) {
//       console.error('Failed to submit:', error);
//     }
    
//     setIsLoading(false);
//     setShowSuccess(true);
//     setPhoneNumber('');
//   };

//   return (
//     <div className="app-container">
//       {/* Floating Background Elements */}
//       <div className="floating-elements">
//         <div className="floating-circle circle-1"></div>
//         <div className="floating-circle circle-2"></div>
//         <div className="floating-circle circle-3"></div>
//       </div>

//       <div className="content-wrapper">
//         {/* Header with Logo */}
//         <header className="header">
//           <div className="logo-section">
//             <img 
//               src="https://image2url.com/images/1758185046787-549ef537-216c-408a-91b0-51d04dec902f.png" 
//               alt="Bizzap Logo" 
//               className="logo-image"
//             />
//             <h1 className="logo">bizzap</h1>
//           </div>
//           <p className="tagline">Turn your sourcing from static to social</p>
//         </header>

//         {/* Main Content */}
//         <main className="main-content">
//           {/* Hero Section */}
//           <div className="hero-section">
//             <h2 className="hero-title">
//               Post requirements<br />
//               Find leads<br />
//               Connect with business
//             </h2>
//             <div className="hero-subtitle">
//               Join the waitlist and get 3 months premium subscription for free
//             </div>
//           </div>
          
//           {/* Premium Features */}
//           <div className="premium-badge">
//             <h3 className="premium-title">Bizzap Premium (Free)</h3>
//             <ul className="premium-features">
//               <li>Get free leads</li>
//               <li>Company Verified Badge</li>
//               <li>Product Catalogue (up-to 10)</li>
//               <li>AI Business Assistant</li>
//               <li>Referral leader board</li>
//             </ul>
//           </div>

//           {/* Phone Form */}
//           <div className="waitlist-form">
//             {!showSuccess ? (
//               <form onSubmit={handleSubmit}>
//                 <div className="form-group">
//                   <div className="input-wrapper">
//                     <Phone className="input-icon" />
//                     <input
//                       type="tel"
//                       value={phoneNumber}
//                       onChange={(e) => setPhoneNumber(e.target.value)}
//                       placeholder="Enter your phone number"
//                       className="form-input"
//                       required
//                     />
//                   </div>
//                 </div>
//                 <button 
//                   type="submit" 
//                   className="join-button"
//                   disabled={isLoading || !phoneNumber.trim()}
//                 >
//                   {isLoading ? (
//                     <div className="loading-content">
//                       <div className="spinner"></div>
//                       <span>Processing...</span>
//                     </div>
//                   ) : (
//                     <div className="button-content">
//                       <Send className="button-icon" />
//                       <span>Join Waitlist - FREE Premium</span>
//                     </div>
//                   )}
//                 </button>
//               </form>
//             ) : (
//               <div className="success-message">
//                 <CheckCircle className="success-icon" />
//                 <div className="success-text">
//                   <strong>Welcome aboard!</strong><br />
//                   You're now on the waitlist. We'll notify you when Bizzap launches!
//                 </div>
//               </div>
//             )}
//           </div>
//         </main>

//         {/* Footer */}
//         {/* <footer className="footer">
//           © 2025 Bizzap. All rights reserved.
//         </footer> */}
//       </div>
//     </div>
//   );
// }

// export default App;


// src/App.js
import React, { useState } from 'react';
import { Phone, Send, CheckCircle, MessageCircle, ArrowRight, X } from 'lucide-react';
import './App.css';

function App() {
  const [phoneNumber, setPhoneNumber] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const [showSuccessPopup, setShowSuccessPopup] = useState(false);

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (!phoneNumber.trim()) return;
    
    setIsLoading(true);
    
    // Submit to Google Forms
    const formData = new FormData();
    formData.append('entry.1658933364', phoneNumber);
    
    try {
      await fetch('https://docs.google.com/forms/u/0/d/e/1FAIpQLSfGsdHitQ5v18ZnCcLMZ3WvTc_GAoZKXkJCFVHbI70ph2J0kQ/formResponse', {
        method: 'POST',
        mode: 'no-cors',
        body: formData
      });
    } catch (error) {
      console.error('Failed to submit:', error);
    }
    
    setIsLoading(false);
    setShowSuccessPopup(true);
    setPhoneNumber('');
  };

  const handleClosePopup = () => {
    setShowSuccessPopup(false);
  };

  const handleJoinWhatsApp = () => {
    window.open('https://chat.whatsapp.com/F5j2hxwXxpDE1BeMLKG8lZ?mode=ems_wa_t', '_blank');
    setShowSuccessPopup(false);
  };

  return (
    <div className="app-container">
      {/* Floating Background Elements */}
      <div className="floating-elements">
        <div className="floating-circle circle-1"></div>
        <div className="floating-circle circle-2"></div>
        <div className="floating-circle circle-3"></div>
      </div>

      <div className="content-wrapper">
        {/* Header with Logo */}
        <header className="header">
          <div className="logo-section">
            <img 
              src="https://image2url.com/images/1758185046787-549ef537-216c-408a-91b0-51d04dec902f.png" 
              alt="Bizzap Logo" 
              className="logo-image"
            />
            <h1 className="logo">bizzap</h1>
          </div>
          <p className="tagline">Turn your sourcing from static to social</p>
        </header>

        {/* Main Content */}
        <main className="main-content">
          {/* Hero Section */}
          <div className="hero-section">
            <h2 className="hero-title">
              Post requirements<br />
              Find leads<br />
              Connect with business
            </h2>
            <div className="hero-subtitle">
              Join the waitlist and get 3 months premium subscription for free
            </div>
          </div>
          
          {/* Premium Features */}
          <div className="premium-badge">
            <h3 className="premium-title">Bizzap Premium (Free)</h3>
            <ul className="premium-features">
              <li>Get free leads</li>
              <li>Company Verified Badge</li>
              <li>Product Catalogue (up-to 10)</li>
              <li>AI Business Assistant</li>
              <li>Referral leader board</li>
            </ul>
          </div>

          {/* Phone Form */}
          <div className="waitlist-form">
            <form onSubmit={handleSubmit}>
              <div className="form-group">
                <div className="input-wrapper">
                  <Phone className="input-icon" />
                  <input
                    type="tel"
                    value={phoneNumber}
                    onChange={(e) => setPhoneNumber(e.target.value)}
                    placeholder="Enter your phone number"
                    className="form-input"
                    required
                  />
                </div>
              </div>
              <button 
                type="submit" 
                className="join-button"
                disabled={isLoading || !phoneNumber.trim()}
              >
                {isLoading ? (
                  <div className="loading-content">
                    <div className="spinner"></div>
                    <span>Processing...</span>
                  </div>
                ) : (
                  <div className="button-content">
                    <Send className="button-icon" />
                    <span>Join Waitlist - FREE Premium</span>
                  </div>
                )}
              </button>
            </form>
          </div>
        </main>
      </div>

      {/* Success Popup Modal */}
      {showSuccessPopup && (
        <div className="popup-overlay">
          <div className="popup-container">
            {/* Close Button */}
            <button onClick={handleClosePopup} className="popup-close-btn">
              <X className="w-5 h-5" />
            </button>

            {/* Success Content */}
            <div className="popup-content">
              <CheckCircle className="popup-success-icon" />
              <h3 className="popup-title">Welcome aboard!</h3>
              <p className="popup-message">
                You're now on the waitlist. We'll notify you when Bizzap launches!
              </p>

              {/* Action Buttons */}
              <div className="popup-buttons">
                <button 
                  onClick={handleJoinWhatsApp}
                  className="whatsapp-btn"
                >
                  <MessageCircle className="w-4 h-4" />
                  <span>Join WhatsApp Group</span>
                  <ArrowRight className="w-4 h-4" />
                </button>
                
                <button 
                  onClick={handleClosePopup}
                  className="skip-btn"
                >
                  Skip for now
                </button>
              </div>

              {/* Additional Info */}
              <p className="popup-info">
                Get instant updates on launch + exclusive features!
              </p>
            </div>
          </div>
        </div>
      )}
    </div>
  );
}

export default App;