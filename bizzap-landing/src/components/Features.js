// src/components/Features.js
import React from "react";

const Features = () => {
  const features = [
    "Get free leads",
    "Company Verified Badge",
    "Product Catalogue (up-to 10)",
    "AI Business Assistant",
    "Referral leader board",
  ];

  return (
    <section className="max-w-2xl mx-auto my-16 md:my-24">
      <div className="bg-white/5 backdrop-blur-md rounded-xl p-8 border border-white/10 shadow-lg animate-scroll">
        <h3 className="text-3xl md:text-4xl font-lato font-bold mb-8 text-brand-yellow text-center">
          Bizzap Premium (Free)
        </h3>
        <div className="space-y-5">
          {features.map((feature, index) => (
            <div key={index} className="flex items-center space-x-4">
              <span className="text-brand-yellow text-xl">✓</span>
              <p className="text-lg md:text-xl font-nunito text-brand-off-white">
                {feature}
              </p>
            </div>
          ))}
        </div>
      </div>
    </section>
  );
};

export default Features;