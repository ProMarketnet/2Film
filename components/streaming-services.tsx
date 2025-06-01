"use client"

import Image from "next/image"
import { useState } from "react"

interface StreamingService {
  name: string
  logo: string
  bgColor: string
  description: string
  price?: string
}

const streamingServices: StreamingService[] = [
  {
    name: "Netflix",
    logo: "/placeholder.svg?height=80&width=80&text=N&bg=e50914&color=white",
    bgColor: "bg-red-600",
    description: "Movies, TV shows, and Netflix Originals",
    price: "From $6.99/month",
  },
  {
    name: "Disney+",
    logo: "/placeholder.svg?height=80&width=80&text=D%2B&bg=113ccf&color=white",
    bgColor: "bg-blue-600",
    description: "Disney, Marvel, Star Wars, and more",
    price: "From $7.99/month",
  },
  {
    name: "Prime Video",
    logo: "/placeholder.svg?height=80&width=80&text=Prime&bg=00a8e1&color=white",
    bgColor: "bg-blue-500",
    description: "Amazon Prime Video content",
    price: "From $8.99/month",
  },
  {
    name: "Apple TV+",
    logo: "/placeholder.svg?height=80&width=80&text=TV%2B&bg=000000&color=white",
    bgColor: "bg-black",
    description: "Apple Original series and films",
    price: "From $6.99/month",
  },
  {
    name: "Hulu",
    logo: "/placeholder.svg?height=80&width=80&text=hulu&bg=1ce783&color=white",
    bgColor: "bg-green-500",
    description: "Current TV shows and movies",
    price: "From $7.99/month",
  },
  {
    name: "Max",
    logo: "/placeholder.svg?height=80&width=80&text=MAX&bg=7b2cbf&color=white",
    bgColor: "bg-purple-600",
    description: "HBO, Warner Bros, and Max Originals",
    price: "From $9.99/month",
  },
  {
    name: "Paramount+",
    logo: "/placeholder.svg?height=80&width=80&text=P%2B&bg=0064ff&color=white",
    bgColor: "bg-blue-700",
    description: "CBS, Paramount, and live sports",
    price: "From $5.99/month",
  },
  {
    name: "Peacock",
    logo: "/placeholder.svg?height=80&width=80&text=Peacock&bg=000000&color=white",
    bgColor: "bg-black",
    description: "NBCUniversal content and live TV",
    price: "From $5.99/month",
  },
  {
    name: "Crunchyroll",
    logo: "/placeholder.svg?height=80&width=80&text=CR&bg=ff6600&color=white",
    bgColor: "bg-orange-600",
    description: "Anime and manga content",
    price: "From $7.99/month",
  },
  {
    name: "Fubo",
    logo: "/placeholder.svg?height=80&width=80&text=fubo&bg=000000&color=white",
    bgColor: "bg-black",
    description: "Live TV and sports streaming",
    price: "From $74.99/month",
  },
  {
    name: "Starz",
    logo: "/placeholder.svg?height=80&width=80&text=STARZ&bg=000000&color=white",
    bgColor: "bg-black",
    description: "Premium movies and series",
    price: "From $9.99/month",
  },
  {
    name: "Showtime",
    logo: "/placeholder.svg?height=80&width=80&text=SHO&bg=ff0000&color=white",
    bgColor: "bg-red-600",
    description: "Premium entertainment and sports",
    price: "From $10.99/month",
  },
]

export function StreamingServicesSection() {
  const [showAll, setShowAll] = useState(false)
  const displayedServices = showAll ? streamingServices : streamingServices.slice(0, 8)

  return (
    <section className="relative z-10 px-4 lg:px-8 pb-12">
      <div className="max-w-6xl mx-auto">
        <div className="text-center mb-8">
          <h2 className="text-gray-400 text-lg mb-2">Streaming services on Film4You</h2>
          <p className="text-gray-500 text-sm">
            Find where to watch across {streamingServices.length}+ streaming platforms
          </p>
        </div>

        <div className="grid grid-cols-2 sm:grid-cols-3 md:grid-cols-4 lg:grid-cols-6 xl:grid-cols-8 gap-4 lg:gap-6">
          {displayedServices.map((service, index) => (
            <div key={index} className="group cursor-pointer" title={service.name}>
              <div className="relative bg-gray-800/50 rounded-lg p-4 hover:bg-gray-700/50 transition-all duration-300 group-hover:scale-105">
                <div className="flex flex-col items-center text-center">
                  <Image
                    src={service.logo || "/placeholder.svg"}
                    alt={`${service.name} logo`}
                    width={60}
                    height={60}
                    className="rounded-lg mb-3 opacity-90 group-hover:opacity-100 transition-opacity duration-300"
                  />
                  <h3 className="text-white text-sm font-medium mb-1">{service.name}</h3>
                  <p className="text-gray-400 text-xs text-center line-clamp-2 mb-2">{service.description}</p>
                  {service.price && <p className="text-teal-400 text-xs font-medium">{service.price}</p>}
                </div>

                {/* Hover overlay */}
                <div className="absolute inset-0 bg-gradient-to-t from-teal-400/20 to-transparent opacity-0 group-hover:opacity-100 transition-opacity duration-300 rounded-lg"></div>
              </div>
            </div>
          ))}
        </div>

        {/* Show More/Less Button */}
        <div className="text-center mt-8">
          <button
            onClick={() => setShowAll(!showAll)}
            className="bg-gray-800 hover:bg-gray-700 text-white px-6 py-3 rounded-lg transition-colors duration-300 focus:outline-none focus:ring-2 focus:ring-teal-400"
          >
            {showAll ? "Show Less" : `See All ${streamingServices.length} Services`}
          </button>
        </div>

        {/* Popular combinations */}
        <div className="mt-12 bg-gray-900/50 rounded-lg p-6">
          <h3 className="text-white text-lg font-medium mb-4 text-center">Popular Streaming Bundles</h3>
          <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
            <div className="bg-gray-800/50 rounded-lg p-4 text-center">
              <div className="flex justify-center space-x-2 mb-3">
                <Image
                  src="/placeholder.svg?height=30&width=30&text=D%2B&bg=113ccf&color=white"
                  alt="Disney+"
                  width={30}
                  height={30}
                  className="rounded"
                />
                <Image
                  src="/placeholder.svg?height=30&width=30&text=hulu&bg=1ce783&color=white"
                  alt="Hulu"
                  width={30}
                  height={30}
                  className="rounded"
                />
              </div>
              <h4 className="text-white text-sm font-medium">Disney Bundle</h4>
              <p className="text-gray-400 text-xs">Disney+ & Hulu</p>
              <p className="text-teal-400 text-sm font-medium mt-1">$9.99/month</p>
            </div>

            <div className="bg-gray-800/50 rounded-lg p-4 text-center">
              <div className="flex justify-center space-x-2 mb-3">
                <Image
                  src="/placeholder.svg?height=30&width=30&text=Prime&bg=00a8e1&color=white"
                  alt="Prime"
                  width={30}
                  height={30}
                  className="rounded"
                />
                <Image
                  src="/placeholder.svg?height=30&width=30&text=N&bg=e50914&color=white"
                  alt="Netflix"
                  width={30}
                  height={30}
                  className="rounded"
                />
              </div>
              <h4 className="text-white text-sm font-medium">Streaming Duo</h4>
              <p className="text-gray-400 text-xs">Prime + Netflix</p>
              <p className="text-teal-400 text-sm font-medium mt-1">$15.98/month</p>
            </div>

            <div className="bg-gray-800/50 rounded-lg p-4 text-center">
              <div className="flex justify-center space-x-2 mb-3">
                <Image
                  src="/placeholder.svg?height=30&width=30&text=MAX&bg=7b2cbf&color=white"
                  alt="Max"
                  width={30}
                  height={30}
                  className="rounded"
                />
                <Image
                  src="/placeholder.svg?height=30&width=30&text=SHO&bg=ff0000&color=white"
                  alt="Showtime"
                  width={30}
                  height={30}
                  className="rounded"
                />
              </div>
              <h4 className="text-white text-sm font-medium">Premium Pack</h4>
              <p className="text-gray-400 text-xs">Max + Showtime</p>
              <p className="text-teal-400 text-sm font-medium mt-1">$19.98/month</p>
            </div>
          </div>
        </div>
      </div>
    </section>
  )
}
