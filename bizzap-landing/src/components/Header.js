// src/components/Header.js
import React from 'react';

// No longer importing the logo from a local file

const Header = () => {
  return (
    <header className="px-6 pt-8 pb-4 text-center flex flex-col items-center">
      <img 
        src="https://image2url.com/images/1758185046787-549ef537-216c-408a-91b0-51d04dec902f.png" 
        alt="Bizzap Logo" 
        className="h-16 w-16 md:h-20 md:w-20 mb-4" 
      />
      <p className="text-xl md:text-2xl text-bizzap-yellow font-nunito">
        Turn your sourcing from static to social
      </p>
    </header>
  );
};

export default Header;