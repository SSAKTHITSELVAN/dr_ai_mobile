// src/components/Hero.js
import React from "react";

const Hero = () => {
  return (
    <section className="text-center max-w-2xl mx-auto my-16 md:my-24 animate-scroll">
      <h2 className="text-4xl md:text-6xl font-lato font-extrabold mb-10 leading-tight text-white">
        Post requirements
        <br />
        Find leads
        <br />
        Connect with business
      </h2>
      <div className="bg-white/5 backdrop-blur-md rounded-xl p-6 border border-white/10 shadow-lg">
        <h3 className="text-2xl md:text-3xl font-lato font-bold text-brand-yellow">
          Join the waitlist and get 3 months premium subscription for free
        </h3>
      </div>
    </section>
  );
};

export default Hero;