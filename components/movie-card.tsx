"use client"

import Image from "next/image"
import { useState } from "react"
import { Play, Plus, Info, Star } from "lucide-react"
import { Button } from "@/components/ui/button"
import StreamingLogo from "./streaming-logo"

interface MovieCardProps {
  title: string
  year: string
  rating: number
  genre: string
  description: string
  imageUrl: string
  streamingServices: string[]
  isHorizontal?: boolean
}

export function MovieCard({
  title,
  year,
  rating,
  genre,
  description,
  imageUrl,
  streamingServices,
  isHorizontal = false,
}: MovieCardProps) {
  const [imageLoaded, setImageLoaded] = useState(false)
  const [imageError, setImageError] = useState(false)

  return (
    <div className={`group cursor-pointer ${isHorizontal ? "flex-shrink-0 w-48" : ""}`}>
      <div className="relative aspect-[2/3] bg-gray-800 rounded-lg overflow-hidden">
        {/* Loading Skeleton */}
        {!imageLoaded && !imageError && (
          <div className="absolute inset-0 bg-gradient-to-r from-gray-800 via-gray-700 to-gray-800 animate-pulse">
            <div className="absolute inset-0 bg-gradient-to-r from-transparent via-gray-600/20 to-transparent animate-shimmer"></div>
          </div>
        )}

        {/* Main Image */}
        {!imageError && (
          <Image
            src={imageUrl || "/placeholder.svg"}
            alt={`${title} poster`}
            fill
            sizes={isHorizontal ? "192px" : "(max-width: 640px) 50vw, (max-width: 1024px) 33vw, 16vw"}
            className={`object-cover group-hover:scale-105 transition-all duration-300 ${
              imageLoaded ? "opacity-100" : "opacity-0"
            }`}
            onLoad={() => setImageLoaded(true)}
            onError={() => setImageError(true)}
            loading="lazy"
            placeholder="blur"
            blurDataURL="data:image/svg+xml;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVR42mNkYPhfDwAChwGA60e6kgAAAABJRU5ErkJggg=="
          />
        )}

        {/* Error State */}
        {imageError && (
          <div className="absolute inset-0 bg-gray-800 flex items-center justify-center">
            <div className="text-center">
              <div className="w-12 h-12 bg-gray-700 rounded-lg flex items-center justify-center mb-2">
                <Play className="w-6 h-6 text-gray-500" />
              </div>
              <p className="text-gray-500 text-xs">{title}</p>
            </div>
          </div>
        )}

        {/* Year Badge */}
        <div className="absolute top-2 right-2 bg-black/70 text-white text-xs px-2 py-1 rounded backdrop-blur-sm">
          {year}
        </div>

        {/* Rating Badge */}
        <div className="absolute top-2 left-2 bg-black/70 text-white text-xs px-2 py-1 rounded backdrop-blur-sm flex items-center gap-1">
          <Star className="w-3 h-3 fill-yellow-400 text-yellow-400" />
          {rating}
        </div>

        {/* Hover Overlay */}
        <div className="absolute inset-0 bg-gradient-to-t from-black/90 via-black/50 to-black/20 opacity-0 group-hover:opacity-100 transition-all duration-300 flex flex-col justify-end p-3">
          {/* Content Info */}
          <div className="mb-3">
            <div className="flex items-center gap-2 mb-2">
              <span className="text-teal-400 text-sm font-bold">{rating}</span>
              <span className="text-white text-xs">• {genre}</span>
            </div>
            <p className="text-white text-xs line-clamp-2 mb-3">{description}</p>

            {/* Streaming Services */}
            <div className="flex gap-1 mb-3">
              {streamingServices.slice(0, 3).map((service, index) => (
                <div key={index} title={service}>
                  <StreamingLogo service={service} size={24} />
                </div>
              ))}
              {streamingServices.length > 3 && (
                <div className="w-6 h-6 bg-gray-600 rounded-sm flex items-center justify-center">
                  <span className="text-white text-xs">+{streamingServices.length - 3}</span>
                </div>
              )}
            </div>
          </div>

          {/* Action Buttons */}
          <div className="flex gap-2">
            <Button size="sm" className="bg-teal-400 text-black hover:bg-teal-500 flex-1 h-8 text-xs">
              <Play className="w-3 h-3 mr-1" />
              Watch
            </Button>
            <Button size="sm" variant="outline" className="border-white/30 text-white hover:bg-white/10 h-8 px-2">
              <Plus className="w-3 h-3" />
            </Button>
            <Button size="sm" variant="outline" className="border-white/30 text-white hover:bg-white/10 h-8 px-2">
              <Info className="w-3 h-3" />
            </Button>
          </div>
        </div>
      </div>

      {/* Title */}
      <h3 className="text-white text-sm mt-2 font-medium truncate" title={title}>
        {title}
      </h3>
    </div>
  )
}
