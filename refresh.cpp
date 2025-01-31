#include <iostream>
#include <fstream>
#include <math.h>
#include <string>
#include <map>
#include <vector>
 
//compile with -mwindows
 
using namespace std;
 
//nomi "costanti" dei file da modificare
const string FOS = "//pl//list.txt"; 	//figure of speech
const string TURN = "output.txt";	//current turn
const string PLAYERS = "//gm//stats.txt";
ifstream PATH ("path.txt");
 
//prototipi
double sigmoid(double);							//funzioni matematiche
double invertedSigmoid(double);
void loadMap(ifstream&, map<string, double>&);
void stampMap(ofstream&, map<string, double>&);
double getValue(string, char); 
string getString(string, char);
int findChar(string, char);
string getpath(ifstream&);
 
void refresh(string);
void update(map<string, double>&);
 
//main
int main(){	
	refresh(getpath(PATH));
}
 
void refresh(string path){
	ifstream figOfSpeechI (path + FOS);
	map<string, double> List;
	loadMap(figOfSpeechI, List);
	figOfSpeechI.close();
	update(List);
	ofstream figOfSpeechO (path + FOS);
	stampMap(figOfSpeechO, List);
}
 
void update(map<string, double>& List){
	for(pair<string, double> x: List){
		if(invertedSigmoid(x.second)>0)
			List[x.first] = sigmoid((int)sqrt(invertedSigmoid(x.second)));
		else
			List[x.first] = sigmoid((int)sqrt(invertedSigmoid(x.second)*-1.0)*-1.0);
	}
}
 
double sigmoid(double x){
	return 10.0/(1.0 + pow(1.6, -x)) +10.0;
}
 
double invertedSigmoid(double x){
	return -log((20.0-x)/(x-10.0))/log(1.6);
}
 
int findChar(string str, char c){
	int i=0;
	while(str[i]!=c && i<str.length()) i++;
	return i;
}
 
double getValue(string str, char c){
	double value=0;
	int powOfTen = 1;
	for(int i=findChar(str, ';')+1; i<str.length(); i++){
		if(str[i]!='.'){
			value += (str[i]-48)*pow(10, powOfTen);
			powOfTen--;
		}
	}
	return value;
}
 
string getString(string str, char c){
	int ID = findChar(str, c);
	string result = "";
	for(int i=0; i<ID; i++){
		result+= str[i];
	} 
	return result;
}
 
void loadMap(ifstream& file, map<string, double>& Map){
	string s;
	while(getline(file, s)){
		double f = getValue(s, ';');
		Map[getString(s, ';')] = f;		
	}
 
}
 
void stampMap(ofstream& file, map<string, double>& Map){
	for(pair<string, double> x: Map){
		file<<x.first<<";"<<x.second<<endl;
	}
 
}
 
string getpath(ifstream& file){
	string s;
	getline(file, s);
	return s;
}
