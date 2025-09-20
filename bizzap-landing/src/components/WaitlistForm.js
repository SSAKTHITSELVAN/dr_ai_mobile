// // src/components/WaitlistForm.js
// import React, { useState } from 'react';

// const WaitlistForm = () => {
//   const [showWhatsApp, setShowWhatsApp] = useState(false);
//   const [phoneNumber, setPhoneNumber] = useState('');

//   const handleSubmit = async (e) => {
//     e.preventDefault();
    
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
    
//     // Show WhatsApp link regardless of submission success
//     setShowWhatsApp(true);
//     setPhoneNumber('');
//   };

//   return (
//     <>
//       {/* Waitlist Form Section */}
//       <section className="px-6 py-12 max-w-md mx-auto">
//         <div className="space-y-4">
//           <input
//             type="text"
//             value={phoneNumber}
//             onChange={(e) => setPhoneNumber(e.target.value)}
//             placeholder="Enter your phone number"
//             className="w-full px-4 py-4 rounded-lg text-black text-base md:text-lg focus:outline-none focus:ring-2 focus:ring-yellow-400"
//           />
//           <button
//             onClick={handleSubmit}
//             className="w-full bg-yellow-400 text-blue-900 font-bold text-base md:text-lg py-4 px-6 rounded-lg hover:bg-yellow-300 transition-colors duration-200 focus:outline-none focus:ring-2 focus:ring-yellow-300"
//           >
//             Prebook Now
//           </button>
//         </div>
//       </section>

//       {/* WhatsApp Link Section */}
//       {showWhatsApp && (
//         <section className="px-6 py-8 max-w-md mx-auto">
//           <div className="text-center">
//             <a
//               href="https://chat.whatsapp.com/F5j2hxwXxpDE1BeMLKG8lZ?mode=ems_wa_t"
//               target="_blank"
//               rel="noopener noreferrer"
//               className="inline-block bg-green-500 hover:bg-green-600 text-white font-bold text-base md:text-lg py-4 px-8 rounded-lg transition-colors duration-200 focus:outline-none focus:ring-2 focus:ring-green-300"
//             >
//               👉 Join Our WhatsApp Group
//             </a>
//             <p className="text-sm text-white/80 mt-4">
//               Or continue browsing below
//             </p>
//           </div>
//         </section>
//       )}
//     </>
//   );
// };

// export default WaitlistForm;


// src/components/WaitlistForm.js
import React, { useState } from 'react';
import { Phone, Send, CheckCircle, MessageCircle, ArrowRight, Users } from 'lucide-react';

const WaitlistForm = () => {
  const [showWhatsApp, setShowWhatsApp] = useState(false);
  const [phoneNumber, setPhoneNumber] = useState('');
  const [isLoading, setIsLoading] = useState(false);

  const handleSubmit = async (e) => {
    e.preventDefault();
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
    // Show WhatsApp link regardless of submission success
    setShowWhatsApp(true);
    setPhoneNumber('');
  };

  return (
    <div className="space-y-3">
      {!showWhatsApp ? (
        <div className="space-y-3">
          <div className="relative">
            <Phone className="absolute left-3 top-1/2 transform -translate-y-1/2 w-4 h-4 text-gray-500" />
            <input
              type="tel"
              value={phoneNumber}
              onChange={(e) => setPhoneNumber(e.target.value)}
              placeholder="Enter your phone number"
              className="w-full pl-10 pr-4 py-3 rounded-xl text-black text-sm md:text-base font-semibold focus:outline-none focus:ring-2 focus:ring-brand-yellow/50 border-2 border-transparent focus:border-brand-yellow transition-all duration-300 shadow-lg placeholder-gray-500"
              required
            />
          </div>
          
          <button
            onClick={handleSubmit}
            disabled={isLoading || !phoneNumber.trim()}
            className="w-full bg-gradient-to-r from-brand-yellow to-orange-400 hover:from-yellow-300 hover:to-orange-300 text-black font-bold text-sm md:text-base py-3 px-4 rounded-xl transition-all duration-300 focus:outline-none focus:ring-2 focus:ring-yellow-300/50 shadow-xl transform hover:scale-105 active:scale-95 disabled:opacity-50 disabled:cursor-not-allowed disabled:transform-none"
          >
            {isLoading ? (
              <div className="flex items-center justify-center space-x-2">
                <div className="w-4 h-4 border-2 border-black border-t-transparent rounded-full animate-spin"></div>
                <span>Processing...</span>
              </div>
            ) : (
              <span className="flex items-center justify-center space-x-2">
                <Send className="w-4 h-4" />
                <span>Prebook Now - 3 Months FREE!</span>
              </span>
            )}
          </button>
          
          <div className="text-center">
            <p className="text-xs text-gray-300 font-nunito flex items-center justify-center space-x-1">
              <Users className="w-3 h-3" />
              <span>Join 1000+ businesses on waitlist</span>
            </p>
          </div>
        </div>
      ) : (
        <div className="text-center space-y-3 animate-fadeIn">
          <div className="bg-gradient-to-r from-green-500/20 to-emerald-500/20 backdrop-blur-md rounded-xl p-4 border border-green-400/30">
            <CheckCircle className="w-12 h-12 text-green-400 mx-auto mb-2 animate-bounce" />
            <h4 className="text-lg md:text-xl font-lato font-bold text-green-400 mb-1">
              Welcome Aboard!
            </h4>
            <p className="text-xs md:text-sm text-green-300 font-nunito">
              You're now part of the Bizzap revolution!
            </p>
          </div>
          
          <a
            href="https://chat.whatsapp.com/F5j2hxwXxpDE1BeMLKG8lZ?mode=ems_wa_t"
            target="_blank"
            rel="noopener noreferrer"
            className="inline-block w-full bg-gradient-to-r from-green-500 to-green-600 hover:from-green-400 hover:to-green-500 text-white font-bold text-sm md:text-base py-3 px-4 rounded-xl transition-all duration-300 focus:outline-none focus:ring-2 focus:ring-green-300/50 shadow-xl transform hover:scale-105 active:scale-95"
          >
            <span className="flex items-center justify-center space-x-2">
              <MessageCircle className="w-4 h-4" />
              <span>Join WhatsApp Community</span>
              <ArrowRight className="w-4 h-4" />
            </span>
          </a>
          
          <div className="bg-gradient-to-r from-blue-500/20 to-purple-500/20 backdrop-blur-md rounded-lg p-3 border border-blue-400/30">
            <p className="text-xs text-blue-300 font-nunito font-semibold flex items-center justify-center space-x-1">
              <CheckCircle className="w-3 h-3" />
              <span>Get instant updates on launch + exclusive features!</span>
            </p>
          </div>
        </div>
      )}
    </div>
  );
};

export default WaitlistForm;