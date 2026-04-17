import React from 'react';
import { FaGithub, FaLinkedin, FaEnvelope } from 'react-icons/fa';
import { portfolioData } from '../../data/portfolioData';

export const Footer: React.FC = () => {
  return (
    <footer className="bg-gray-900 text-white py-12">
      <div className="container mx-auto px-4 sm:px-6 lg:px-8">
        <div className="grid grid-cols-1 md:grid-cols-3 gap-8 mb-8">
          <div>
            <h3 className="text-xl font-bold mb-4">About</h3>
            <p className="text-gray-400 leading-relaxed">
              {portfolioData.personalInfo.about}
            </p>
          </div>

          <div>
            <h3 className="text-xl font-bold mb-4">Quick Links</h3>
            <ul className="space-y-2">
              <li><a href="#about" className="text-gray-400 hover:text-white transition-colors">About</a></li>
              <li><a href="#experience" className="text-gray-400 hover:text-white transition-colors">Experience</a></li>
              <li><a href="#skills" className="text-gray-400 hover:text-white transition-colors">Skills</a></li>
              <li><a href="#projects" className="text-gray-400 hover:text-white transition-colors">Projects</a></li>
              <li><a href="#education" className="text-gray-400 hover:text-white transition-colors">Education</a></li>
              <li><a href="#contact" className="text-gray-400 hover:text-white transition-colors">Contact</a></li>
            </ul>
          </div>

          <div>
            <h3 className="text-xl font-bold mb-4">Connect</h3>
            <div className="flex space-x-4">
              <a
                href={portfolioData.contact.github}
                target="_blank"
                rel="noopener noreferrer"
                className="w-10 h-10 bg-gray-800 rounded-full flex items-center justify-center hover:bg-primary transition-colors duration-200"
              >
                <FaGithub className="w-5 h-5" />
              </a>
              <a
                href={portfolioData.contact.linkedin}
                target="_blank"
                rel="noopener noreferrer"
                className="w-10 h-10 bg-gray-800 rounded-full flex items-center justify-center hover:bg-primary transition-colors duration-200"
              >
                <FaLinkedin className="w-5 h-5" />
              </a>
              <a
                href={`mailto:${portfolioData.contact.email}`}
                className="w-10 h-10 bg-gray-800 rounded-full flex items-center justify-center hover:bg-primary transition-colors duration-200"
              >
                <FaEnvelope className="w-5 h-5" />
              </a>
            </div>
          </div>
        </div>

        <div className="border-t border-gray-800 pt-8 text-center text-gray-400">
          <p>&copy; {new Date().getFullYear()} {portfolioData.personalInfo.name}. All rights reserved.</p>
        </div>
      </div>
    </footer>
  );
};
