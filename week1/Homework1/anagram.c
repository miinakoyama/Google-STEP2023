#include <stdio.h>
#include <string.h>
#include <stdlib.h>

void	swap(char *a, char *b) {
	char	tmp;

	tmp = *b;
	*b = *a;
	*a = tmp;
}

//1単語をソートする
void	sort_word(char *word[], int left, int right)
{
	char	pivot; //閾値
	int		i;
	int		j;

	if (left >= right)
		return ;
	pivot = *word[left];
	i = left;
	j = right;
	while (1)
	{
		//左から閾値以上の数字を探索
		while (*word[i] < pivot)
			i++;
		//右から閾値以下の数字を探索
		while (*word[j] > pivot)
			j--;
		//終了条件
		if (i >= j)
			break ;
	swap(word[i], word[j]);
	i++;
	j--;
	}
	//左側をソート
	sort_word(word, left, i - 1);
	//右側をソート
	sort_word(word, j + 1, right);
}

// int	binary_search(char *word, char *dict[], int start, int end)
// {

// }

int main(void)
{
	char	*word;
	char	**dict;
	int		d_size;
	int		i;

	//辞書ファイルを読み込む
	FILE *fp = fopen("words.txt", "r");
	if (fp == NULL){
		printf("Error opening file (words.txt)\n");
		return (1);
	}
	//辞書のサイズ取得
	fscanf(fp, "%d", &d_size); //取得できてない
	printf("%d\n", d_size);
	dict = (char **)malloc(sizeof(char *) * d_size);

	i = 0;
	while (i < d_size)
	{
		fscanf(fp, "%s", dict[i]);
		dict[i] = (char *)malloc(sizeof(char) * strlen(dict[i]));
	}

	//入力ファイルを読み込む
	FILE *fp = fopen("input.txt", "r");
	if (fp == NULL){
		printf("Error opening file (input.txt)\n");
		return (1);
	}
	return (0);
}