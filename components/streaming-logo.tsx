interface StreamingLogoProps {
  service: string
  size?: number
}

export default function StreamingLogo({ service, size = 60 }: StreamingLogoProps) {
  const logoConfig = {
    Netflix: {
      bg: "bg-red-600",
      text: "N",
      textColor: "text-white",
      font: "font-bold text-2xl",
    },
    "Disney+": {
      bg: "bg-blue-600",
      text: "D+",
      textColor: "text-white",
      font: "font-bold text-lg",
    },
    "Prime Video": {
      bg: "bg-blue-500",
      text: "Prime",
      textColor: "text-white",
      font: "font-bold text-xs",
    },
    "Apple TV+": {
      bg: "bg-black",
      text: "TV+",
      textColor: "text-white",
      font: "font-bold text-sm",
    },
    Hulu: {
      bg: "bg-green-500",
      text: "hulu",
      textColor: "text-white",
      font: "font-bold text-sm",
    },
    Max: {
      bg: "bg-purple-600",
      text: "MAX",
      textColor: "text-white",
      font: "font-bold text-sm",
    },
    "Paramount+": {
      bg: "bg-blue-700",
      text: "P+",
      textColor: "text-white",
      font: "font-bold text-lg",
    },
    Peacock: {
      bg: "bg-gradient-to-r from-blue-500 to-green-400",
      text: "🦚",
      textColor: "text-white",
      font: "text-2xl",
    },
    Crunchyroll: {
      bg: "bg-orange-600",
      text: "CR",
      textColor: "text-white",
      font: "font-bold text-lg",
    },
    Fubo: {
      bg: "bg-black",
      text: "fubo",
      textColor: "text-white",
      font: "font-bold text-xs",
    },
    Starz: {
      bg: "bg-black",
      text: "STARZ",
      textColor: "text-white",
      font: "font-bold text-xs",
    },
    Showtime: {
      bg: "bg-red-600",
      text: "SHO",
      textColor: "text-white",
      font: "font-bold text-sm",
    },
  }

  const config = logoConfig[service as keyof typeof logoConfig] || {
    bg: "bg-gray-600",
    text: service.charAt(0),
    textColor: "text-white",
    font: "font-bold text-lg",
  }

  return (
    <div
      className={`${config.bg} rounded-lg flex items-center justify-center ${config.textColor} ${config.font} shadow-lg`}
      style={{ width: size, height: size }}
      title={service}
    >
      {config.text}
    </div>
  )
}
