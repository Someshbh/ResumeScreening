export interface Candidate {
    candidateName: string;
    candidateEmail: string;
    candidateMobile:string;
    matchingPercentage: number;
    missingSkills: string[];
    candidateSkills: string[];
    totalYearsOfExperience: number | string;
    experienceSummary: string;
    isExpanded?: boolean;
    isSkillsExpanded: boolean;
    isMissingSkillsExpanded: boolean;
}
  
export interface TokenDetail {
    modality: string;
    tokenCount: number;
}
  
export interface UsageMetadata {
    promptTokenCount: number;
    candidatesTokenCount: number;
    totalTokenCount: number;
    promptTokensDetails: TokenDetail[];
    candidatesTokensDetails: TokenDetail[];
}
  
export interface GeminiResponse {
    candidates: Candidate[];
    usageMetadata?: UsageMetadata;
    modelVersion: string;
}
  