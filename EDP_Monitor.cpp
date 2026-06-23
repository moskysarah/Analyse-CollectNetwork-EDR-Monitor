#include <iostream>
#include <windows.h>
#include <tlhelp32.h>
#include <fstream>
#include <chrono>
#include <thread>
#include <string>

// Fonction pour convertir un tableau de wchar_t en string standard
std::string WStringToString(const std::wstring& wstr) {
    if (wstr.empty()) return std::string();
    int size_needed = WideCharToMultiByte(CP_UTF8, 0, &wstr[0], (int)wstr.size(), NULL, 0, NULL, NULL);
    std::string strTo(size_needed, 0);
    WideCharToMultiByte(CP_UTF8, 0, &wstr[0], (int)wstr.size(), &strTo[0], size_needed, NULL, NULL);
    return strTo;
}

void LogActiveProcess() {
    // Création d'un snapshot de tous les processus du système
    HANDLE hProcessSnap = CreateToolhelp32Snapshot(TH32CS_SNAPPROCESS, 0);
    if (hProcessSnap == INVALID_HANDLE_VALUE) {
        std::cerr << "[-] Erreur lors du snapshot des processus." << std::endl;
        return;
    }

    PROCESSENTRY32 pe32;
    pe32.dwSize = sizeof(PROCESSENTRY32);

    // Récupération du premier processus
    if (!Process32First(hProcessSnap, &pe32)) {
        CloseHandle(hProcessSnap);
        return;
    }

    std::ofstream logFile("process_log.txt", std::ios_base::app);
    if (!logFile.is_open()) {
        std::cerr << "[-] Impossible d'ouvrir le fichier de log." << std::endl;
        CloseHandle(hProcessSnap);
        return;
    }

    // Boucle à travers tous les processus
    do {
        std::wstring wName(pe32.szExeFile);
        std::string processName = WStringToString(wName);
        
        // On écrit au format : PID|NOM_PROCESSUS
        logFile << pe32.th32ProcessID << "|" << processName << std::endl;

    } while (Process32Next(hProcessSnap, &pe32));

    logFile.close();
    CloseHandle(hProcessSnap);
}

int main() {
    std::cout << "[+] SpyGuard EDR (C++) active. Surveillance active..." << std::endl;
    
    // Le capteur prend une capture toutes les 5 secondes
    while (true) {
        LogActiveProcess();
        std::this_thread::sleep_for(std::chrono::seconds(5));
    }
    
    return 0;
}