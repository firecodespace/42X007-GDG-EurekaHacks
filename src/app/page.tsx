export default function Home() {
  return (
    <div className="relative flex min-h-screen items-center justify-center overflow-hidden bg-[#0a1628] font-['Space_Grotesk']">

      {/* Gradient Background */}
      <div
        aria-hidden
        className="absolute inset-0 blur-[80px]"
        style={{
          background: `
            linear-gradient(135deg,
              rgba(111, 0, 255, 0.5) 0%,
              transparent 25%,
              transparent 50%,
              rgba(99, 255, 188, 0.5) 75%,
              rgba(99, 255, 188, 0.6) 100%
            ),
            linear-gradient(135deg,
              rgba(111, 0, 255, 0.4) 0%,
              rgba(111, 0, 255, 0.2) 15%,
              transparent 40%
            ),
            linear-gradient(135deg,
              transparent 60%,
              rgba(99, 255, 188, 0.3) 85%,
              rgba(99, 255, 188, 0.4) 100%
            ),
            #0a1628
          `,
        }}
      />

      {/* Content */}
      <div className="headings">
        <h1 className="relative z-10 text-center text-[72px] font-semibold tracking-[-0.02em] text-white md:text-[48px]">
          Welcome to HackFilx
        </h1>
        <h2 className="relative z-10 text-center text-[62px] tracking-[-0.02em] text-white md:text-[48px]">
          Coming Soon!
        </h2>
      </div>
    </div>
  );
}
