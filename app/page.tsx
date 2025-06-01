"use client"

import { Button } from "@/components/ui/button"
import { useState } from "react"
import { AIChatWidget } from "@/components/ai-chat"
import { AISearchBar } from "@/components/ai-search-bar"
import StreamingLogo from "@/components/streaming-logo"

export default function Film4YouLanding() {
  const [searchResults, setSearchResults] = useState<any>(null)
  const [showAIResults, setShowAIResults] = useState(false)

  const streamingServices = [
    { name: "Netflix" },
    { name: "Disney+" },
    { name: "Prime Video" },
    { name: "Apple TV+" },
    { name: "Hulu" },
    { name: "Max" },
    { name: "Paramount+" },
    { name: "Peacock" },
    { name: "Crunchyroll" },
    { name: "Fubo" },
    { name: "Starz" },
    { name: "Showtime" },
  ]

  const handleAIResults = (results: any) => {
    setSearchResults(results)
    setShowAIResults(true)
  }

  return (
    <div className="min-h-screen bg-black text-white">
      {/* Header */}
      <header className="relative z-10 flex items-center justify-between p-4 lg:px-8">
        <div className="flex items-center space-x-8">
          {/* Logo */}
          <div className="flex items-center space-x-2">
            <div className="w-8 h-8 bg-teal-400 flex items-center justify-center rounded-md">
              <div className="w-0 h-0 border-l-[6px] border-l-transparent border-r-[6px] border-r-transparent border-b-[8px] border-b-black" />
            </div>
            <span className="text-xl font-bold text-teal-400">Film4You</span>
          </div>

          {/* Navigation */}
          <nav className="hidden md:flex items-center space-x-6">
            <a
              href="#"
              className="text-white hover:text-teal-400 transition-colors focus:outline-none focus:ring-2 focus:ring-teal-400 rounded"
            >
              New
            </a>
            <a
              href="#"
              className="text-gray-400 hover:text-teal-400 transition-colors focus:outline-none focus:ring-2 focus:ring-teal-400 rounded"
            >
              Popular
            </a>
            <a
              href="#"
              className="text-gray-400 hover:text-teal-400 transition-colors focus:outline-none focus:ring-2 focus:ring-teal-400 rounded"
            >
              Sports
            </a>
            <a
              href="#"
              className="text-gray-400 hover:text-teal-400 transition-colors focus:outline-none focus:ring-2 focus:ring-teal-400 rounded"
            >
              Guide
            </a>
          </nav>
        </div>

        <div className="flex items-center space-x-4">
          {/* AI-Powered Search Bar */}
          <div className="hidden lg:block">
            <AISearchBar onResults={handleAIResults} />
          </div>

          {/* Login Button */}
          <Button
            variant="outline"
            className="border-gray-600 text-white hover:bg-teal-400 hover:text-black hover:border-teal-400 focus:ring-2 focus:ring-teal-400"
          >
            Sign In
          </Button>
        </div>
      </header>

      {/* Hero Section */}
      <main className="relative z-10 flex flex-col items-center justify-center min-h-[70vh] px-4 text-center">
        <h1 className="text-4xl md:text-6xl lg:text-7xl font-bold mb-6 max-w-4xl leading-tight">
          Your streaming guide for movies, TV shows & sports
        </h1>

        <p className="text-lg md:text-xl text-gray-300 mb-8 max-w-3xl">
          Find your favourite films and shows from past to present with Film4You. Whether you're searching for golden
          age classics, cult favourites from the '80s, or today's latest releases, our extensive library spans decades
          of cinematic history.
        </p>

        <p className="text-lg md:text-xl text-gray-300 mb-12 max-w-2xl font-medium">
          Every era of entertainment at your fingertips.
        </p>

        <div className="flex flex-col sm:flex-row gap-4">
          <Button
            size="lg"
            className="bg-teal-400 text-black hover:bg-teal-500 px-8 py-3 text-lg font-semibold focus:ring-2 focus:ring-teal-400"
          >
            Discover Movies & TV shows
          </Button>
          <Button
            size="lg"
            variant="outline"
            className="border-gray-600 text-white hover:bg-white hover:text-black px-8 py-3 text-lg focus:ring-2 focus:ring-white"
          >
            Features
          </Button>
        </div>
      </main>

      {/* AI Search Results Modal */}
      {showAIResults && searchResults && (
        <div className="fixed inset-0 bg-black/80 z-50 flex items-center justify-center p-4">
          <div className="bg-gray-900 rounded-lg max-w-3xl w-full max-h-[80vh] overflow-y-auto">
            <div className="p-6">
              <div className="flex justify-between items-center mb-4">
                <h2 className="text-xl font-bold text-teal-400">AI Search Results</h2>
                <Button
                  onClick={() => setShowAIResults(false)}
                  variant="ghost"
                  className="text-gray-400 hover:text-white focus:ring-2 focus:ring-teal-400"
                >
                  ✕
                </Button>
              </div>

              <div className="space-y-4">
                <div className="bg-gray-800 rounded-lg p-4">
                  <div className="flex items-start space-x-3">
                    <div className="w-8 h-8 bg-teal-400 rounded-full flex items-center justify-center flex-shrink-0">
                      <span className="text-black font-bold text-sm">AI</span>
                    </div>
                    <div className="flex-1">
                      <p className="text-gray-300 mb-3">
                        <strong>Your search:</strong> "{searchResults.query}"
                      </p>
                      <div className="text-white text-sm whitespace-pre-wrap mb-4">{searchResults.response}</div>

                      {searchResults.suggestions && searchResults.suggestions.length > 0 && (
                        <div className="space-y-2">
                          <p className="text-gray-400 text-sm font-medium">Quick actions:</p>
                          {searchResults.suggestions.map((suggestion: string, index: number) => (
                            <div
                              key={index}
                              className="bg-gray-700 rounded p-3 hover:bg-gray-600 cursor-pointer transition-colors focus:outline-none focus:ring-2 focus:ring-teal-400"
                              tabIndex={0}
                            >
                              <p className="text-white text-sm">{suggestion}</p>
                            </div>
                          ))}
                        </div>
                      )}

                      <div className="mt-4 flex flex-wrap gap-2">
                        <Button
                          size="sm"
                          className="bg-teal-400 text-black hover:bg-teal-500 focus:ring-2 focus:ring-teal-400"
                        >
                          Find Similar Titles
                        </Button>
                        <Button
                          size="sm"
                          variant="outline"
                          className="border-gray-600 text-white hover:bg-gray-700 focus:ring-2 focus:ring-gray-400"
                        >
                          Refine Search
                        </Button>
                        <Button
                          size="sm"
                          variant="outline"
                          className="border-gray-600 text-white hover:bg-gray-700 focus:ring-2 focus:ring-gray-400"
                        >
                          Add to Watchlist
                        </Button>
                      </div>
                    </div>
                  </div>
                </div>

                <div className="bg-gray-800 rounded-lg p-4">
                  <h3 className="text-white font-medium mb-3">Ask AI anything about entertainment:</h3>
                  <div className="grid grid-cols-1 sm:grid-cols-2 gap-2">
                    <div className="text-left p-2 bg-gray-700 rounded">
                      <span className="text-teal-400 text-sm">🎬 "What are Tarantino's best films?"</span>
                    </div>
                    <div className="text-left p-2 bg-gray-700 rounded">
                      <span className="text-teal-400 text-sm">📺 "Shows like Breaking Bad"</span>
                    </div>
                    <div className="text-left p-2 bg-gray-700 rounded">
                      <span className="text-teal-400 text-sm">🏆 "Oscar winners from the 90s"</span>
                    </div>
                    <div className="text-left p-2 bg-gray-700 rounded">
                      <span className="text-teal-400 text-sm">🎭 "Best film noir classics"</span>
                    </div>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
      )}

      {/* Streaming Services Section */}
      <section className="relative z-10 px-4 lg:px-8 py-16">
        <div className="max-w-6xl mx-auto">
          <h2 className="text-center text-gray-400 text-lg mb-8">Streaming services on Film4You</h2>

          <div className="flex flex-wrap justify-center items-center gap-6 lg:gap-8">
            {streamingServices.map((service, index) => (
              <div key={index} className="flex-shrink-0 group cursor-pointer" title={service.name}>
                <div className="relative">
                  <StreamingLogo service={service.name} size={60} />
                  {/* Service name tooltip on hover */}
                  <div className="absolute -bottom-8 left-1/2 transform -translate-x-1/2 bg-black/80 text-white text-xs px-2 py-1 rounded opacity-0 group-hover:opacity-100 transition-opacity duration-300 whitespace-nowrap">
                    {service.name}
                  </div>
                </div>
              </div>
            ))}

            {/* See All Button */}
            <div
              className="flex items-center justify-center w-16 h-16 bg-gray-800 rounded-lg cursor-pointer hover:bg-gray-700 transition-colors focus:outline-none focus:ring-2 focus:ring-teal-400 group"
              tabIndex={0}
              title="See all streaming services"
            >
              <div className="text-center">
                <span className="text-gray-400 text-xs font-medium group-hover:text-white transition-colors">SEE</span>
                <br />
                <span className="text-gray-400 text-xs font-medium group-hover:text-white transition-colors">ALL</span>
              </div>
            </div>
          </div>

          {/* Additional streaming info */}
          <div className="text-center mt-6">
            <p className="text-gray-500 text-sm">
              Find where to watch across {streamingServices.length}+ streaming platforms
            </p>
          </div>
        </div>
      </section>

      {/* AI Chat Widget */}
      <AIChatWidget />
    </div>
  )
}
