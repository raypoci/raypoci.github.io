import React from 'react';
import { FaGithub } from 'react-icons/fa';
import { ThemeToggle } from '../ui/ThemeToggle';
import { portfolioData } from '../../data/portfolioData';

export const Header: React.FC = () => {
  return (
    <header className="fixed top-0 left-0 right-0 z-50 bg-white/80 dark:bg-gray-900/80 backdrop-blur-md border-b border-gray-100 dark:border-gray-800">
      <nav className="container mx-auto px-4 sm:px-6 lg:px-8">
        <div className="flex items-center justify-between h-16">
          <a href="/" className="flex items-center space-x-2">
            <span className="text-2xl font-bold text-primary">Rei</span>
            <span className="text-xl text-gray-600 dark:text-gray-400">Portfolio</span>
          </a>

          <div className="hidden md:flex items-center space-x-1">
            {portfolioData.navbar.map((item) => (
              <a
                key={item.name}
                href={item.link}
                className="nav-link px-4 py-2 rounded-lg text-sm font-medium text-gray-700 dark:text-gray-300 hover:bg-gray-100 dark:hover:bg-gray-800 hover:text-primary transition-colors duration-200"
              >
                {item.name}
              </a>
            ))}
          </div>

          <div className="flex items-center space-x-2">
            <ThemeToggle />
            <a
              href={portfolioData.contact.github}
              target="_blank"
              rel="noopener noreferrer"
              className="p-2 rounded-lg text-gray-600 dark:text-gray-400 hover:bg-gray-100 dark:hover:bg-gray-800 hover:text-primary transition-colors duration-200"
              aria-label="GitHub"
            >
              <FaGithub className="w-5 h-5" />
            </a>
          </div>
        </div>
      </nav>
    </header>
  );
};
