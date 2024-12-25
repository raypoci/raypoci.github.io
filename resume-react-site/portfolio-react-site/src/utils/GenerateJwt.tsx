import jwt from "jsonwebtoken";
import fs from "fs";
import path from "path";

export const generateJwt = (): string => {
  const privateKeyPath = path.resolve(__dirname, "../private-key.pem");
  const privateKey = fs.readFileSync(privateKeyPath, "utf8");

  const payload = {
    iss: "your-app-id", // Your GitHub App ID
    iat: Math.floor(Date.now() / 1000),
    exp: Math.floor(Date.now() / 1000) + 10 * 60, // 10 minutes expiration
    aud: "api.github.com",
  };

  const token = jwt.sign(payload, privateKey, { algorithm: "RS256" });
  return token;
};
