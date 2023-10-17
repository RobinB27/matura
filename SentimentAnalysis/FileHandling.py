# Copyright (C) 2022 Robin Bacher and Lucien Gees
# This file is part of the "Automated Stock Trading Using News Headlines" matura project.
# Last edited on 17/10/2023

# This file implements several utiltiy functions which are needed for interacting
# with the FinancialPhraseBank dataset. This dataset is used to train the Naive Bayes Classifier
# which provides the Sentiment Classification of news Head lines for the bot.

class FileHandling:
    def parseLine(line: str) -> list:
        """Utility Function that converts line read from dataset to format that can be used by the NaiveBayes Classifier
        
        Args:
            line (String): line read from dataset
        
        Returns:
            List: Data that can be fed to the Classifier
        """
        
        # Token and label are seperated by @ in this dataset
        strings = line.split("@")
        
        token = strings[0]
        label = strings[1]
        
        # Remove EOL from Label
        label = label.replace("\n", "")
                    
        tokendict = {}
        tokendict[token] = True
        
        output = [
            tokendict, label
        ]
        
        return output

    def readData() -> list:
        """Reads the dataset and returns a list containing all data in a format usable by the NaiveBayes Classifier

        Returns:
            list: Full usable dataset
        """
        dirPath = "SentimentAnalysis/FinancialPhraseBank"
        fileNames = [
            "Sentences_50Agree.txt",
            "Sentences_66Agree.txt",
            "Sentences_75Agree.txt",
            "Sentences_AllAgree.txt",
        ]
        
        dataset = []
        for name in fileNames:
            
            filePath = dirPath + "/" + name
            with open(filePath, "r") as file:
                lines = file.readlines()
                
                for line in lines:
                    data = FileHandling.parseLine(line)
                    dataset.append(data)
        
        return dataset
