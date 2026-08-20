using Godot;
using System;
using System.Collections.Generic;
using System.Text.RegularExpressions;
using System.Linq;
using Microsoft.VisualBasic.FileIO;

// declare a CsvEntry class to hold row information for each item in the dataset
// these are just dataset containers, will be created with object initializer syntax
public class CsvEntry
{
	public string Column1;
	public string Column2;
	public HashSet<string> Column3Values;
	public HashSet<string> Column4Values;
}

public partial class RecEngine : Node
{	
	// set up a List<CsvEntry> that will hold the dataset
	private List<CsvEntry> _dataset = new List<CsvEntry>();
	
	// set up a Dictionary<string, CsvEntry> to use as a lookup table for game input validation
	private Dictionary<string, CsvEntry> _lookup;
	
	// create an empty List to hold potential candidates before final recommendations
	// the string is the game's name and the float is the similarity score
	// list should only hold 20 values for now
	private List<(string name, float score)> _potential = new List<(string, float)>();
	private int _potentialLimit = 19;

	// create an empty HashSet to hold final recommendations
	private HashSet<string> _final = new HashSet<string>();
	
	public override void _Ready()
	{
		// store the absolute path to the dataset
		// doesn't work with exported .exe, program can't find it
		// string path = ProjectSettings.GlobalizePath("res://dataset/dataset.csv");
		
		// retrieves full path for dataset.csv, assumes .csv is located in same folder as .exe
		string path = System.IO.Path.Combine(OS.GetExecutablePath().GetBaseDir(), "dataset.csv");
		
		// create the parser
		using var parser = new TextFieldParser(path)
		{
			TextFieldType = FieldType.Delimited,
			HasFieldsEnclosedInQuotes = false
		};
		parser.SetDelimiters(",");
		
		// read through parser until all values are read from CSV
		while (!parser.EndOfData) 
		{
			string[] fields = parser.ReadFields();
			// create a new CsvEntry for each row in the CSV file and add to dataset
			// the genre and tag columns contain semicolons and need to be delineated further
			// Column3Values and Column4Values are converted to HashSet before addition
			CsvEntry row = new CsvEntry
			{
				Column1 = fields[1].Trim(),
				Column2 = fields[2].Trim(),
				Column3Values = fields[3]
					.Split(';', StringSplitOptions.RemoveEmptyEntries)
					.Select(s => s.Trim())
					.ToHashSet(),
				Column4Values = fields[4]
					.Split(';', StringSplitOptions.RemoveEmptyEntries)
					.Select(s => s.Trim())
					.ToHashSet()
			};
			
			// dataset includes empty name cells and unusable characters
			// add the current row to the dataset only if the name field is readable
			if (!string.IsNullOrEmpty(row.Column1) && Regex.IsMatch(row.Column1, @"^[A-Za-z0-9.,\s-]+$"))
			{
				_dataset.Add(row);
			}
		}
				
		// create the lookup Dictionary from the dataset
		_lookup = _dataset
			// the game's name is the key for the lookup Dictionary
			// uses GroupBy to combine all rows that share name values
			.GroupBy(g => g.Column1)
			// after GroupBy call g refers to the group
			// Key targets the string, First targets the first object in the group
			.ToDictionary(g => g.Key, g => g.First());
	}
	
	// determines if the submitted game name is found in the dataset
	public bool IsInputValid(string input)
	{
		// returns true if a game is found using the lookup Dictionary
		// we don't need the object returned from the lookup, so _ for second parameter
		bool result = _lookup.TryGetValue(input, out _);
		return result;
	}
	
	// handles the individual method calls for a recommendation and returns the result
	public HashSet<string> GenerateRecommendations(string input1, string input2)
	{
		// clear the potential list for new recommendations
		_potential.Clear();
		
		(CsvEntry game1, CsvEntry game2) inputs = GetInputMatches(input1, input2);
		foreach (var entry in _dataset)
		{
			// pair the candidate game name with the similarity score and add to potential list
			// filter out the input games so they aren't added to potential list
			if (entry != inputs.Item1 && entry != inputs.Item2)
			{
				AddPotentialList(entry.Column1, GetSimilarityScore(inputs.Item1, inputs.Item2, entry));
			}
		}
		
		GenerateFinal();
		return _final;
	}
	
	// retrieves the game objects from the dataset that match each input
	// assumes each input string has already been validated by IsInputValid
	// GenerateRecommendations calls this: CsvEntry (game1, game2) = GetInputMaches("game1", "game2")
	public (CsvEntry game1, CsvEntry game2) GetInputMatches(string input1, string input2)
	{
		// find the matching game object for each input from the dataset
		CsvEntry game1 = _dataset.FirstOrDefault(entry => entry.Column1 == input1);
		CsvEntry game2 = _dataset.FirstOrDefault(entry => entry.Column1 == input2);
		return (game1, game2);
	}
	
	public float GetSimilarityScore(CsvEntry game1, CsvEntry game2, CsvEntry game3)
	{
		// game3 is the candidate game from the dataset
		// cumulative similarity score is: genreScore + tagScore + devScore
		// devScore is either 0.5f or 0 (just a small boost to score)
		// perfect genreScore and tagScore values are more important
		float score = 0.0f;
		
		// local count variables to hold intersection and union values
		int intersectionCount = 0;
		int unionCount = 0;
		// local bool variables to determine if a game has a genre/tag
		bool inGame1 = false;
		bool inGame2 = false;
		bool inGame3 = false;
		
		// cadidate genres and tags are held in Column3Values and Column4Values, respectively
		// Jaccardian similarity is intersection over union
		// create a local allItems variable to hold the distinct contents of the genre/tag attributes for each game
		var allItems = game1.Column3Values.Concat(game2.Column3Values).Concat(game3.Column3Values).Distinct();
		foreach(var item in allItems)
		{
			inGame1 = game1.Column3Values.Contains(item);
			inGame2 = game2.Column3Values.Contains(item);
			inGame3 = game3.Column3Values.Contains(item);
			// if an item is found in all three games, increase intersectionCount
			intersectionCount += (inGame1 && inGame2 && inGame3) ? 1 : 0;
			// every item in allItems is a part of the union, increment every iteration
			unionCount++;
		}
		
		// add the results of Jaccard similarity operation to score
		score += (unionCount == 0) ? 0f : (float)intersectionCount / unionCount;
		
		allItems = game1.Column4Values.Concat(game2.Column4Values).Concat(game3.Column4Values).Distinct();
		foreach(var item in allItems)
		{
			inGame1 = game1.Column4Values.Contains(item);
			inGame2 = game2.Column4Values.Contains(item);
			inGame3 = game3.Column4Values.Contains(item);
			intersectionCount += (inGame1 && inGame2 && inGame3) ? 1 : 0;
			unionCount++;
		}
		
		score += (unionCount == 0) ? 0f : (float)intersectionCount / unionCount;

		// add 0.5f if the candidate game developer matches one of the input games
		score += (game3.Column2 == game1.Column2) ? 0.5f : 0f;
		score += (game3.Column2 == game2.Column2) ? 0.5f : 0f;

		return score;
	}
	
	public void AddPotentialList(string name, float score)
	{
		// FindIndex searches for the first element where the condition is true
		// if the condition is not met FindIndex returns -1
		int index = _potential.FindIndex(e => score > e.score);
		if (index == -1)
		{
			_potential.Add((name, score));
		}
		else
		{
			_potential.Insert(index, (name, score));
		}
		
		// trim the potential list if necessary to keep at 20 items
		if (_potential.Count > 20)
		{
			_potential.RemoveAt(20);
		}
	}
	
	public void GenerateFinal()
	{
		Random rand = new Random();
		int[] indexes = new int[5];
		
		// clear any existing contents in the final list
		_final.Clear();
		
		// randomly generates five index values up to _potentialLimit and stores in array
		// adds the game name corresponding to each index value to _final
		for (int i = 0; i < 5; i++)
		{
			indexes[i] = rand.Next(_potentialLimit);
			_final.Add(_potential[indexes[i]].Item1);
		}
	}	
}
