export const metadata = {
  title: "FinSight",
  description: "Legal Intelligence for MSMEs"
};

export default function RootLayout({ children }) {
  return (
    <html lang="en">
      <body>{children}</body>
    </html>
  );
}
