#include <stdio.h>
#include <string.h>

typedef struct _Endereco Endereco;

struct _Endereco {
  char logradouro[72];
  char bairro[72];
  char cidade[72];
  char uf[72];
  char sigla[2];
  char cep[8];
  char lixo[2]; // Ao Espaço no final da linha + quebra de linha
};

int main(int argc, char **argv) {
  FILE *f;
  Endereco e;
  int qt;
  int c;
  long num_enderecos;
  int endereco_dir;
  int endereco_esq, endereco_meio = 0;

  if (argc != 2) {
    fprintf(stderr, "USO: %s [CEP]", argv[0]);
    return 1;
  }

  c = 0;
  printf("Tamanho da Estrutura: %ld\n\n", sizeof(Endereco));
  f = fopen("cep_ordenado.dat", "rb");
  fseek(f, 0, SEEK_END);
  num_enderecos = ftell(f) / sizeof(Endereco);
  endereco_dir = num_enderecos;
  endereco_meio = num_enderecos / 2;
  printf("Endereco do meio: %d\n", endereco_meio);
    

  // vai pro inicio do endereco que esta no meio do arquivo
  fseek(f, endereco_meio * sizeof(Endereco), SEEK_SET);

  qt = fread(&e, sizeof(Endereco), 1, f);

  while (qt > 0) {
    c++;

    e.logradouro[71] = '\0';
    
    // pode usar o strstr
    if (strncmp(argv[1], e.cep, 8) == 0) {
      printf("%.72s\n%.72s\n%.72s\n%.72s\n%.2s\n%.8s\n", e.logradouro, e.bairro,
             e.cidade, e.uf, e.sigla, e.cep);
      break;
    } else if (strncmp(argv[1], e.cep, 8) < 0) {
        endereco_dir = endereco_meio - 1;
        printf("Menor, endereco meio: %d\n", endereco_meio);
    } else if (strncmp(argv[1], e.cep, 8) > 0) {
        endereco_esq = endereco_meio + 1;
        printf("Maior, endereco meio: %d\n", endereco_meio);
    }
    endereco_meio = (endereco_dir + endereco_esq) / 2;

    fseek(f, endereco_meio * sizeof(Endereco), SEEK_SET);
    qt = fread(&e, sizeof(Endereco), 1, f);
  }
  printf("Total Lido: %d\n", c);
  fclose(f);
}
