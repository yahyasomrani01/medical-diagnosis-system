import React from 'react';

const Header = () => {
    return (
        <div className="bg-white border-b border-gray-200">
            <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-6">
                <div className="flex items-center gap-4">
                    {/* Medical Icon */}
                    <div className="flex-shrink-0">
                        <div className="w-14 h-14 bg-primary-600 rounded-2xl flex items-center justify-center shadow-md">
                            <svg className="w-8 h-8 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M4.318 6.318a4.5 4.5 0 000 6.364L12 20.364l7.682-7.682a4.5 4.5 0 00-6.364-6.364L12 7.636l-1.318-1.318a4.5 4.5 0 00-6.364 0z" />
                            </svg>
                        </div>
                    </div>

                    {/* Title */}
                    <div>
                        <h1 className="text-2xl font-bold text-gray-900">
                            Système de Diagnostic Médical
                        </h1>
                        <p className="text-gray-600 text-sm">
                            Analyse basée sur l'Intelligence Artificielle
                        </p>
                    </div>
                </div>
            </div>
        </div>
    );
};

export default Header;
