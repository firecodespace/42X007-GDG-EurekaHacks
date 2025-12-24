import Image from "next/image";

export default function Home() {
  return (
    <>
      {/* ===== STATIC BACKGROUND ===== */}
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
      <main className="relative z-10 flex min-h-screen flex-col items-center px-6 text-center font-['Space_Grotesk'] text-white">

        {/* Logo */}
        <div className="mt-10 mb-20 sm:mt-12 sm:mb-24">
          <Image
            src="/images/hackflix-high-resolution-logo-transparent.png"
            alt="HackFlix Logo"
            width={220}
            height={80}
            priority
            className="h-auto w-[160px] sm:w-[200px] md:w-[220px]"
          />
        </div>

        {/* Headings */}
        <div className="flex flex-col items-center">
          <h1 className="font-semibold tracking-[-0.02em] 
                         text-[42px] 
                         sm:text-[56px] 
                         md:text-[72px]">
            Welcome to HackFlix
          </h1>

          <h2 className="mt-4 opacity-90 tracking-[-0.02em]
                         text-[28px]
                         sm:text-[36px]
                         md:text-[48px]">
            Coming Soon!
          </h2>
        </div>
      </main>
    </>
  );
}
