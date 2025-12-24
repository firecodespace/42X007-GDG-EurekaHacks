export default function Home() {
  return (
    <>
      {/* ===== STATIC BACKGROUND (ROOT LEVEL) ===== */}
      <div
        aria-hidden
        className="pointer-events-none fixed inset-0 z-0 overflow-hidden"
        style={{ backgroundColor: "#000D2E" }}
      >
        {/* Top diagonal strip */}
        <div
          className="absolute left-[-25%] top-[120px] h-[180px] w-[150%] opacity-90 blur-[70px]"
          style={{
            background:
              "linear-gradient(90deg, rgba(111,0,255,0.8) 8%, rgba(99,255,188,0.88) 88%)",
            transform: "rotate(6deg)",
          }}
        />

        {/* Bottom diagonal strip */}
        <div
          className="absolute left-[-25%] top-[560px] h-[180px] w-[150%] opacity-90 blur-[70px]"
          style={{
            background:
              "linear-gradient(90deg, rgba(111,0,255,0.8) 8%, rgba(99,255,188,0.88) 88%)",
            transform: "rotate(6deg)",
          }}
        />
      </div>

      {/* ===== FOREGROUND CONTENT ===== */}
      <main className="relative z-10 flex min-h-screen flex-col items-center justify-center text-center font-['Space_Grotesk'] text-white">
        <h1 className="text-[72px] font-semibold tracking-[-0.02em] md:text-[48px]">
          Welcome to HackFilx
        </h1>

        <h2 className="mt-4 text-[62px] tracking-[-0.02em] opacity-90 md:text-[42px]">
          Coming Soon!
        </h2>
      </main>
    </>
  );
}
