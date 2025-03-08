import { Component, OnInit } from '@angular/core';
import { JobDescription } from './Models/JobDescription';
import { MainService } from './Services/main.service';
import { Candidate } from './Models/GeminiResponse';
import { trigger, transition, style, animate } from '@angular/animations';

@Component({
  selector: 'app-main',
  templateUrl: './main.component.html',
  styleUrls: ['./main.component.scss'],
  animations: [
    trigger('fadeInOut', [
      transition(':enter', [
        style({ opacity: 0 }),
        animate('300ms', style({ opacity: 1 }))
      ]),
      transition(':leave', [
        animate('300ms', style({ opacity: 0 }))
      ])
    ])
  ]
})
export class MainComponent implements OnInit {
  activeSection: string = 'jobDescription';
  jobDescription: JobDescription = new JobDescription();
  maxResumes: number = 10;
  geminiResponses: Candidate[] = [];
  filteredCandidates: Candidate[] = [];
  searchTerm: string = '';
  isLoading: boolean = false;

  constructor(private mainService: MainService) {}

  ngOnInit(): void {
    this.filteredCandidates = this.geminiResponses;
  }

  showSection(section: string): void {
    this.activeSection = section;
  }

  // Form validation
  isFormValid(): boolean {
    return (
      !!this.jobDescription.jobTitle &&
      !!this.jobDescription.minExperience &&
      !!this.jobDescription.qualification &&
      !!this.jobDescription.requiredSkills &&
      !!this.jobDescription.description &&
      this.jobDescription.resumes.length > 0
    );
  }

  // Handle file selection
  onFileSelected(event: Event): void {
    const element = event.target as HTMLInputElement;
    const files = element.files;

    if (!files) return;

    for (let i = 0; i < files.length; i++) {
      const file = files[i];

      if (this.jobDescription.resumes.length >= this.maxResumes) {
        this.showError('Maximum limit reached', 'You can upload a maximum of 10 resumes.');
        return;
      }

      if (file.type !== 'application/pdf') {
        this.showError('Invalid file type', `File "${file.name}" is not supported. Only PDFs are allowed.`);
        continue;
      }

      this.jobDescription.resumes.push(file);
    }

    // Reset file input
    element.value = '';
  }

  // Remove resume
  removeResume(index: number): void {
    this.jobDescription.resumes.splice(index, 1);
  }

  // Filter candidates based on search term
  filterCandidates(): void {
    if (!this.searchTerm) {
      this.filteredCandidates = this.geminiResponses;
      return;
    }

    const searchLower = this.searchTerm.toLowerCase();
    this.filteredCandidates = this.geminiResponses.filter(candidate => 
      candidate.candidateName.toLowerCase().includes(searchLower) ||
      candidate.experienceSummary.toLowerCase().includes(searchLower) ||
      candidate.missingSkills?.some(skill => skill.toLowerCase().includes(searchLower))
    );
  }

  submitJobDescription() {
    if (!this.isFormValid()) {
      return;
    }

    const formData = new FormData();
    formData.append('jobTitle', this.jobDescription.jobTitle);
    formData.append('minExperience', this.jobDescription.minExperience.toString());
    formData.append('qualification', this.jobDescription.qualification);
    formData.append('requiredSkills', this.jobDescription.requiredSkills);
    formData.append('description', this.jobDescription.description);

    // Append resumes to FormData
    this.jobDescription.resumes.forEach((file) => {
      formData.append('resumes', file, file.name);
    });

    this.isLoading = true;
    this.mainService.submitJobDescription(formData).subscribe({
      next: (response: any) => {
        console.log('Response:', response); // Debug log
        
        // Transform the response to get candidates array
        this.geminiResponses = this.transformGeminiResponse(response.resume_results || []);
        
        // Sort and set filtered candidates
        this.filteredCandidates = [...this.geminiResponses]
          .sort((a: Candidate, b: Candidate) => b.matchingPercentage - a.matchingPercentage)
          .map((candidate: Candidate) => ({
            ...candidate,
            isExpanded: false
          }));

        this.showSection('details');
        this.isLoading = false;
        this.showSuccess('Success', 'Job Description and resumes analyzed successfully!');
      },
      error: (error: Error) => {
        console.error('Error analyzing resumes:', error);
        this.showError('Error', 'Error analyzing resumes. Please try again.');
        this.isLoading = false;
      }
    });
  }

  // Transform Gemini response
  private transformGeminiResponse(results: any[]): Candidate[] {
    const candidates: Candidate[] = [];
    results.forEach(result => {
      if (result.candidates && result.candidates.length > 0) {
        result.candidates.forEach((cand: any) => {
          const candidate: Candidate = {
            candidateName: cand["Candidate's Name"] || '',
            candidateEmail: cand["Candidate's Email"] || '',
            candidateMobile: cand["Candidate's Mobile"] || '',
            matchingPercentage: parseFloat(cand["Matching Percentage"]) || 0,
            missingSkills: cand["Missing Skills"] || [],
            candidateSkills: cand["Candidate's Skills"] || [],
            totalYearsOfExperience: parseFloat(cand["Total Years of Experience"]) || 0,
            experienceSummary: cand["Experience Summary"] || cand["A brief Experience Summary"] || '',
            isExpanded: false,
            isSkillsExpanded: false,
            isMissingSkillsExpanded: false
          };
          candidates.push(candidate);
        });
      }
    });
    return candidates;
  }

  toggleExpand(candidate: Candidate): void {
    candidate.isExpanded = !candidate.isExpanded;
  }

  toggleSkillsExpand(candidate: Candidate): void {
    candidate.isSkillsExpanded = !candidate.isSkillsExpanded;
  }

  toggleMissingSkillsExpand(candidate: Candidate): void {
    candidate.isMissingSkillsExpanded = !candidate.isMissingSkillsExpanded;
  }

  clearForm(): void {
    this.jobDescription = new JobDescription();
    this.isLoading = false;
  }

  // Error handling methods
  private showError(title: string, message: string): void {
    // You can implement your preferred error notification method here
    // For example, using a toast service or a modal
    console.error(title, message);
    // TODO: Implement your preferred notification method
  }

  private showSuccess(title: string, message: string): void {
    // You can implement your preferred success notification method here
    console.log(title, message);
    // TODO: Implement your preferred notification method
  }
}
