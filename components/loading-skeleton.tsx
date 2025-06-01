export function MovieCardSkeleton({ isHorizontal = false }: { isHorizontal?: boolean }) {
  return (
    <div className={`animate-pulse ${isHorizontal ? "flex-shrink-0 w-48" : ""}`}>
      <div className="relative aspect-[2/3] bg-gray-800 rounded-lg overflow-hidden">
        <div className="absolute inset-0 bg-gradient-to-r from-gray-800 via-gray-700 to-gray-800">
          <div className="absolute inset-0 bg-gradient-to-r from-transparent via-gray-600/20 to-transparent animate-shimmer"></div>
        </div>
        <div className="absolute top-2 right-2 bg-gray-700 rounded w-12 h-5"></div>
        <div className="absolute top-2 left-2 bg-gray-700 rounded w-8 h-5"></div>
      </div>
      <div className="mt-2 bg-gray-700 rounded h-4 w-3/4"></div>
    </div>
  )
}

export function ContentSectionSkeleton() {
  return (
    <div className="mb-8">
      <div className="flex items-center justify-between mb-4">
        <div className="bg-gray-700 rounded h-6 w-32 animate-pulse"></div>
        <div className="bg-gray-700 rounded h-5 w-16 animate-pulse"></div>
      </div>
      <div className="flex space-x-4 overflow-hidden">
        {Array.from({ length: 6 }).map((_, index) => (
          <MovieCardSkeleton key={index} isHorizontal={true} />
        ))}
      </div>
    </div>
  )
}
