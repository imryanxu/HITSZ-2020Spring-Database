#include <stdlib.h>
#include <stdio.h>
#include "extmem.h"

typedef struct data_blk{
	int X[7];
    int Y[7];
    int addr;
}data_blk;

int menu(){
    int choice;
	printf("请选择以下一项：\n");
    printf("1.基于线性搜索的关系选择(R.A=30的元组)\n");
	printf("2.两阶段多路归并排序算法（TPMMS）,将关系R和S分别排序\n");
	printf("3.基于索引的关系选择：建立索引文件，选出R.A=30的元组\n");
	printf("4.实现关系投影算法：对关系R上的A属性进行投影并去重\n");
	printf("5.基于排序的连接操作：对关系R和S计算R.A连接S.C\n");
	printf("6.基于排序的集合的交算法\n");
	printf("7.基于排序的集合的并算法\n");
	printf("8.基于排序的集合的差算法R-S\n");
	printf("0.退出\n");
	printf("请输入选项：");
	scanf("%d",&choice);
	return choice;
}


void init_data_blk(data_blk *data){
	int i;
	data -> addr = -1;
	for (i=0; i<7; i++){
		data -> X[i] = -1;
		data -> Y[i] = -1;
	}
}


// 用来读每个blk的信息（7个元组和1个地址）
void read_data_blk(unsigned char *blk, data_blk *data){
	int i=0;
	char str[5];
	for (i = 0; i < 7; i++) //一个blk存7个元组加一个地址
    {

        for (int k = 0; k < 4; k++)
        {
            str[k] = *(blk + i*8 + k);
        }
        data->X[i] = atoi(str);
        for (int k = 0; k < 4; k++)
        {
            str[k] = *(blk + i*8 + 4 + k);
        }
        data->Y[i] = atoi(str);
    }
    for (int k = 0; k < 4; k++)
    {
        str[k] = *(blk + i*8 + k);
    }
    data->addr = atoi(str);
}


//用来写特定result的信息
void write_data_blk(unsigned char *blk, data_blk res){
	int i=0;
	char str[5];
	for (i = 0; i < 7; i++) //一个blk存7个元组加一个地址
    {
		itoa(res.X[i],str,10);
        for (int k = 0; k < 4; k++)
        {
            *(blk + i*8 + k) = str[k];
        }
        itoa(res.Y[i],str,10);
        for (int k = 0; k < 4; k++)
        {
            *(blk + i*8 + 4 + k) = str[k];
        }
    }
	itoa(res.addr,str,10);
    for (int k = 0; k < 4; k++)
    {
        *(blk + i*8 + k) = str[k];
	}
}


int func1(Buffer *buf){
	printf("------------------------------------------------------------\n");
    printf("基于线性搜索的选择算法 R.A=30\n");
    printf("------------------------------------------------------------\n");
	unsigned char *blk;
    unsigned char *result;
	result = getNewBlockInBuffer(buf);	//把满足条件的元组全都记录在result块中
	data_blk data;	//暂存读入的blk的信息
	init_data_blk(&data);
	data_blk res;	//res暂存要写入result的信息
	init_data_blk(&res);
	int count = 0;	//记录R.A=30有多少个元组
	int cur_blk = 1;
	for(cur_blk = 1; cur_blk<=16; cur_blk++){
		if ((blk = readBlockFromDisk(cur_blk, buf)) == NULL)
		{
			perror("Reading Block Failed!\n");
			return -1;
		}
		printf("读入数据块%d\n", cur_blk);
		read_data_blk(blk, &data);
		int i = 0;
		for(i=0; i<8; i++){
			if(data.X[i]==30){
				printf("(X=%d, Y=%d)\n",data.X[i],data.Y[i]);
				res.X[count] = data.X[i];
				res.Y[count] = data.Y[i];
				count++;
			}
		}
		freeBlockInBuffer(blk, buf);
	}
	res.addr = 0;
	write_data_blk(result, res);
	if (writeBlockToDisk(result, 1111, buf) != 0)
    {
        perror("Writing Block Failed!\n");
        return -1;
    }
	printf("注：结果写入磁盘：1111\n\n");
	printf("满足选择条件的元组一共%d个。\n\n", count);
	printf("IO读写一共%ld次。\n\n", buf->numIO);
	freeBlockInBuffer(result, buf);
	return 0;
}


int tpmms(Buffer *buf){
	printf("------------------------------------------------------------\n");
    printf("两阶段多路归并排序算法（TPMMS）,将关系R和S分别排序\n");
    printf("------------------------------------------------------------\n");
	//将关系R（4*4）子集排序，排序后存在101.blk-116.blk
	int i = 1;	//内排序共4轮
	int j = 0;	//每次内排序处理4个块，每块里面7个元组
	int k;	//冒泡排序中需要的
	for (i=1; i<=4; i++){
        data_blk data[4];	//暂存读入的blk的信息
        unsigned char *blk[4];
		for(j=0; j<=3; j++){
            init_data_blk(&data[j]);
		}

		for(j=0; j<=3; j++){
			if ((blk[j] = readBlockFromDisk((i-1)*4+j+1, buf)) == NULL)
			{
				perror("Reading Block Failed!\n");
				return -1;
			}
			read_data_blk(blk[j], &data[j]);	//读取信息结束
		}
		//冒泡排序
		for (k=0; k<27; k++){
			for (j=0; j<27-k; j++){
				if(data[j/7].X[j%7] > data[(j+1)/7].X[(j+1)%7]){
					int tempx, tempy;
					tempx = data[j/7].X[j%7];
					tempy = data[j/7].Y[j%7];
					data[j/7].X[j%7] = data[(j+1)/7].X[(j+1)%7];
					data[j/7].Y[j%7] = data[(j+1)/7].Y[(j+1)%7];
					data[(j+1)/7].X[(j+1)%7] = tempx;
					data[(j+1)/7].Y[(j+1)%7] = tempy;
				}
			}
		}

		//排序后存在101.blk-116.blk
		for(j=0; j<=3; j++){
			data[j].addr = 102+(i-1)*4+j;
			if(i==4&&j==3)	data[j].addr = 0;

			/*
			for(int m=0; m<7; m++){
				printf("%d %d\n", data[j].X[m], data[j].Y[m]);
			}
			printf("%d\n", data[j].addr);
			*/

			write_data_blk(blk[j], data[j]);
			if (writeBlockToDisk(blk[j], 101+(i-1)*4+j, buf) != 0)
			{
				perror("Writing Block Failed!\n");
				return -1;
			}
			freeBlockInBuffer(blk[j], buf);
		}
		// printf("\n");
	}

	//每个子集排序完了再进行归并，归并排序后存在301.blk-316.blk
	unsigned char *blk[4];	//记录4个载入的块
	for (i=0; i<4; i++)
		blk[i] = readBlockFromDisk(i*4+101, buf);
    data_blk ready[4];	//暂存读入的blk的信息

	int group[4];	//记录4个组现在载入了几块
	for (i=0; i<4; i++)
		group[i]=1;

	unsigned char *compare, *output;
	compare = getNewBlockInBuffer(buf); //缓存中比较块
	data_blk cmp;	//暂存比较块的信息
	init_data_blk(&cmp);

	int pointer[4]; //记录载入缓存的块到了哪个元组
	for (i=0; i<4; i++)
		pointer[i]=0;

	output = getNewBlockInBuffer(buf); //缓存中输出块
	data_blk out;	//暂存输出块的信息
	init_data_blk(&out);
	int outnum = 0;	//记录输出块已经记录了多少个数了
	int outaddr = 302;

	while(group[0]<=4||group[1]<=4||group[2]<=4||group[3]<=4){
		//一个块读完了，需要换块
		for (i=0; i<4; i++){
			if(pointer[i]==7){
				if (group[i]<4){
					freeBlockInBuffer(blk[i], buf);
					blk[i] = readBlockFromDisk(i*4+group[i]+101, buf);
					pointer[i] = 0;
				}
				group[i]++;
			}
		}

		int flag[4];	//记录该组是否已经读完了（1是读完了，0未读完）
		for (i=0; i<4; i++){
			if(group[i]<=4)
				flag[i]=0;
			else
				flag[i]=1;
		}

		init_data_blk(&cmp);
		int min = 1001;
		int index = -1;
		for(j=0; j<=3; j++){
			if(!flag[j]){
				init_data_blk(&ready[j]);
				read_data_blk(blk[j], &ready[j]);
				int pos = pointer[j];
				cmp.X[j] = ready[j].X[pos];
				cmp.Y[j] = ready[j].Y[pos];
				if(cmp.X[j]<min){
					index = j;
					min = cmp.X[j];
				}
			}
		}

		write_data_blk(compare, cmp);
		pointer[index] ++;
		out.X[outnum] = cmp.X[index];
		out.Y[outnum] = cmp.Y[index];
		outnum++;
		//如果这次写写满了输出块
		if(outnum==7){
			if(outaddr==317)	outaddr=0;
			out.addr = outaddr;
			/*
			for(int m=0; m<7; m++){
				printf("%d %d\n", out.X[m], out.Y[m]);
			}
			printf("%d\n\n", out.addr);
			*/

			write_data_blk(output, out);
			init_data_blk(&out);
			outnum = 0;
			if(outaddr==0)	outaddr=317;
			writeBlockToDisk(output, outaddr-1, buf);
			outaddr++;
		}
	}
	freeBlockInBuffer(output, buf);
	freeBlockInBuffer(compare, buf);
	for(i=0; i<4; i++){
		freeBlockInBuffer(blk[i], buf);
	}


	//将关系S（4*8）子集排序，排序后存在117.blk-148.blk
	for (i=1; i<=4; i++){
		data_blk data[8];	//暂存读入的blk的信息
		unsigned char *blk[8];
		for(j=0; j<=7; j++){
            init_data_blk(&data[j]);
		}

		for(j=0; j<=7; j++){
			if ((blk[j] = readBlockFromDisk((i-1)*8+j+17, buf)) == NULL)
			{
				perror("Reading Block Failed!\n");
				return -1;
			}
			read_data_blk(blk[j], &data[j]);	//读取信息结束
		}

		//冒泡排序
		for (k=0; k<55; k++){
			for (j=0; j<55-k; j++){
				if(data[j/7].X[j%7] > data[(j+1)/7].X[(j+1)%7]){
					int tempx, tempy;
					tempx = data[j/7].X[j%7];
					tempy = data[j/7].Y[j%7];
					data[j/7].X[j%7] = data[(j+1)/7].X[(j+1)%7];
					data[j/7].Y[j%7] = data[(j+1)/7].Y[(j+1)%7];
					data[(j+1)/7].X[(j+1)%7] = tempx;
					data[(j+1)/7].Y[(j+1)%7] = tempy;
				}
			}
		}

		//排序后存在117.blk-148.blk
		for(j=0; j<=7; j++){
			data[j].addr = 118+(i-1)*8+j;
			if(i==4&&j==7)	data[j].addr = 0;

            /*
			for(int m=0; m<7; m++){
				printf("%d %d\n", data[j].X[m], data[j].Y[m]);
			}
			printf("%d\n", data[j].addr);
            */

			write_data_blk(blk[j], data[j]);
			if (writeBlockToDisk(blk[j], 117+(i-1)*8+j, buf) != 0)
			{
				perror("Writing Block Failed!\n");
				return -1;
			}
			freeBlockInBuffer(blk[j], buf);
		}
		//printf("\n");
	}

	//每个子集排序完了再进行归并，归并排序后存在317.blk-348.blk
	//unsigned char *blk[4];	//记录4个载入的块
	for (i=0; i<4; i++)
		blk[i] = readBlockFromDisk(i*8+117, buf);
    //data_blk ready[4];	//暂存读入的blk的信息

	//int group[4];	//记录4个组现在载入了几块
	for (i=0; i<4; i++)
		group[i]=1;

	//unsigned char *compare, *output;
	compare = getNewBlockInBuffer(buf); //缓存中比较块
	//data_blk cmp;	//暂存比较块的信息
	init_data_blk(&cmp);

	//int pointer[4]; //记录载入缓存的块到了哪个元组
	for (i=0; i<4; i++)
		pointer[i]=0;

	output = getNewBlockInBuffer(buf); //缓存中输出块
	//data_blk out;	//暂存输出块的信息
	init_data_blk(&out);
	outnum = 0;	//记录输出块已经记录了多少个数了
	outaddr = 318;

	while(group[0]<=8||group[1]<=8||group[2]<=8||group[3]<=8){
		//一个块读完了，需要换块
		for (i=0; i<4; i++){
			if(pointer[i]==7){
				if (group[i]<8){
					freeBlockInBuffer(blk[i], buf);
					blk[i] = readBlockFromDisk(i*8+group[i]+117, buf);
					pointer[i] = 0;
				}
				group[i]++;
			}
		}

		int flag[4];	//记录该组是否已经读完了（1是读完了，0未读完）
		for (i=0; i<4; i++){
			if(group[i]<=8)
				flag[i]=0;
			else
				flag[i]=1;
		}

		init_data_blk(&cmp);
		int min = 1001;
		int index = -1;
		for(j=0; j<=3; j++){
			if(!flag[j]){
				init_data_blk(&ready[j]);
				read_data_blk(blk[j], &ready[j]);
				int pos = pointer[j];
				cmp.X[j] = ready[j].X[pos];
				cmp.Y[j] = ready[j].Y[pos];
				if(cmp.X[j]<min){
					index = j;
					min = cmp.X[j];
				}
			}
		}

		write_data_blk(compare, cmp);
		pointer[index] ++;
		out.X[outnum] = cmp.X[index];
		out.Y[outnum] = cmp.Y[index];
		outnum++;
		//如果这次写写满了输出块
		if(outnum==7){
			if(outaddr==349)	outaddr=0;
			out.addr = outaddr;

			/*
			for(int m=0; m<7; m++){
				printf("%d %d\n", out.X[m], out.Y[m]);
			}
			printf("%d\n\n", out.addr);
			*/

			write_data_blk(output, out);
			init_data_blk(&out);
			outnum = 0;
			if(outaddr==0)	outaddr=349;
			writeBlockToDisk(output, outaddr-1, buf);
			outaddr++;
		}
	}
	freeBlockInBuffer(output, buf);
	freeBlockInBuffer(compare, buf);
	for(i=0; i<4; i++){
		freeBlockInBuffer(blk[i], buf);
	}
	printf("关系R排序后输出到文件301.blk到316.blk\n");
	printf("关系S排序后输出到文件317.blk到348.blk\n\n");
	return 0;
}

int setindex(Buffer *buf){
	printf("------------------------------------------------------------\n");
    printf("基于索引的关系选择：建立索引文件，选出R.A=30的元组\n");
    printf("------------------------------------------------------------\n");
	//创建索引
	int i, j;
	int indexnum[41];
	for (i=0; i<41; i++){
		indexnum[i] = 318;
	}

	data_blk index;
	for (i=0; i<6; i++){
		init_data_blk(&index);
	}
	unsigned char *blk, *save;
	save = getNewBlockInBuffer(buf);
	for (i=301; i<317; i++){
		blk = readBlockFromDisk(i, buf);
		data_blk data;
		init_data_blk(&data);
		read_data_blk(blk, &data);
		for (j=0; j<7; j++){
			if (i<indexnum[data.X[j]]){
				indexnum[data.X[j]] = i;
			}
		}
		freeBlockInBuffer(blk, buf);
	}
	int addr = 349;
	int count = 0;
	for (i=1; i<41; i++){
		if(indexnum[i]!=318){
			index.X[count] = i;
			index.Y[count] = indexnum[i];
			count++;
			if(count==7){
				index.addr = addr+1;
				/*
				for(int m=0; m<7; m++){
					printf("%d %d\n", index.X[m], index.Y[m]);
				}
				printf("%d\n\n", index.addr);
				*/
				write_data_blk(save, index);
				writeBlockToDisk(save, addr, buf);
				init_data_blk(&index);
				addr++;
				count = 0;
			}
		}
	}
	if(count>0){
		index.addr = 0;
		/*
		for(int m=0; m<7; m++){
			printf("%d %d\n", index.X[m], index.Y[m]);
		}
		printf("%d\n\n", index.addr);
		*/
		write_data_blk(save, index);
		writeBlockToDisk(save, addr, buf);
	}
	freeBlockInBuffer(save, buf);
    return 0;
}


int func3(Buffer *buf){
	int i, j, pos[2];
	int flag = 0;
	unsigned char *blk, *output;
	data_blk data;

	buf->numIO = 0;

	for (i=349; i<=354; i++){
		blk = readBlockFromDisk(i, buf);
		printf("读入索引块%d\n", i);
		init_data_blk(&data);
		read_data_blk(blk, &data);
		for (j=0; j<8; j++){
			if(data.X[j]==30){
				pos[0] = data.Y[j];
			}
			if(data.X[j]==31){
				pos[1] = data.Y[j];
				flag=1;
			}
		}
		if(flag)
			break;
		else
			printf("没有满足条件的元组。\n");
		freeBlockInBuffer(blk, buf);
	}

	output = getNewBlockInBuffer(buf);
	data_blk out;
	init_data_blk(&out);
	int count = 0;
	for(i=0; i<2; i++){
		blk = readBlockFromDisk(pos[i], buf);
		printf("读入数据块%d\n", pos[i]);
		read_data_blk(blk, &data);
		for (j=0; j<8; j++){
			if(data.X[j]==30){
				out.X[count] = data.X[j];
				out.Y[count] = data.Y[j];
				count++;
				printf("(X=%d, Y=%d)\n", data.X[j], data.Y[j]);
			}
		}
		freeBlockInBuffer(blk, buf);
	}
	out.addr = 0;
	write_data_blk(output, out);
	writeBlockToDisk(output, 3333, buf);
	printf("注：结果写入磁盘：3333\n\n");
	freeBlockInBuffer(output, buf);
	printf("满足选择条件的元组一共%d个。\n\n", count);
	printf("IO读写一共%ld次。\n\n", buf->numIO);

    return 0;
}


int func4(Buffer *buf){
	printf("------------------------------------------------------------\n");
    printf("实现关系投影算法：对关系R上的A属性进行投影并去重\n");
    printf("------------------------------------------------------------\n");
	unsigned char *blk, *output;
	int pre = 0;
	int i,j;
	output = getNewBlockInBuffer(buf);
	data_blk out;
	init_data_blk(&out);
	int count = 0;
	int addr = 401;
	for (i=301; i<317; i++){
		blk = readBlockFromDisk(i, buf);
		printf("读入数据块%d\n", i);
		data_blk data;
		init_data_blk(&data);
		read_data_blk(blk, &data);
		for (j=0; j<7; j++){
			if (data.X[j]!=pre){
				printf("(X=%d)\n", data.X[j]);
				out.X[count] = data.X[j];
				count++;
				pre = data.X[j];
				if(count==7){
					out.addr = addr+1;
					write_data_blk(output, out);
					writeBlockToDisk(output, addr, buf);
					printf("注：结果写入磁盘：%d\n", addr);
					init_data_blk(&out);
					addr++;
					count = 0;
				}
			}
		}
		freeBlockInBuffer(blk, buf);
	}
	if(count>0){
		out.addr = 0;
		write_data_blk(output, out);
		writeBlockToDisk(output, addr, buf);
		printf("注：结果写入磁盘：%d\n", addr);
	}
	printf("\n");
	freeBlockInBuffer(output, buf);
	return 0;
}


int func5(Buffer *buf){
	printf("------------------------------------------------------------\n");
    printf("基于排序的连接操作：对关系R和S计算R.A连接S.C\n");
    printf("------------------------------------------------------------\n");
	unsigned char *blk_r, *compare;
	unsigned char *output[2];
	unsigned char *blk_s[4];
	int i, j, k;
	int group[4]; //S每组已经走了多少块
	int flag[4];	//遍历完毕置为1，遍历没完置为0
	int pointer[4];	//目前在哪个元组
	/*for(i=0; i<4; i++){
		flag[i] = 0;
		pointer[i] = 0;
	}*/
	data_blk data_s[4];
	/*for(i=0; i<4; i++){
		blk_s[i] = readBlockFromDisk(117+i*8, buf);
		group[i] = 1;
	}*/
	compare = getNewBlockInBuffer(buf);
	output[0] = getNewBlockInBuffer(buf);
	output[1] = getNewBlockInBuffer(buf);
	data_blk data_r, cmp;
	data_blk out[2];
	int outnum = 0;	//两块输出块可以输出7对
	init_data_blk(&data_r);
	init_data_blk(&cmp);
	init_data_blk(&out[0]);
	init_data_blk(&out[1]);
	int addr = 501;
	int joinnum = 0;


	for(i=0; i<4; i++){
		init_data_blk(&data_s[i]);
	}
	for(k=301; k<=316; k++){
		blk_r = readBlockFromDisk(k, buf);
		read_data_blk(blk_r, &data_r);

		for (j=0; j<7; j++){
			cmp.X[4] = data_r.X[j];
			if(data_r.X[j]<=19)
				continue;

			cmp.Y[4] = data_r.Y[j];

			for(i=0; i<4; i++){
				flag[i] = 0;
				pointer[i] = 0;
			}
			//data_blk data_s[4];
			for(i=0; i<4; i++){
				blk_s[i] = readBlockFromDisk(117+i*8, buf);
				group[i] = 1;
			}
            //比较块中的比较
			while(!flag[0]||!flag[1]||!flag[2]||!flag[3]){
                //比较块的一次比完
				//一个块读完了，需要换块
				for(i=0; i<4; i++){
					if(pointer[i]==7){
						if (group[i]<8){
							freeBlockInBuffer(blk_s[i], buf);
							blk_s[i] = readBlockFromDisk(i*8+group[i]+117, buf);
							pointer[i] = 0;
						}
						group[i]++;
					}
				}

				//读完了一个组的所有块当然置为1
				for(i=0; i<4; i++){
					if(group[i]>8)
						flag[i]=1;
				}

				int index[4];	//记录哪一组S可以与R连接
				for(i=0; i<=3; i++){
					index[i] = -1;
				}
				for(i=0; i<=3; i++){
					if(!flag[i]){
						read_data_blk(blk_s[i], &data_s[i]);
						int pos = pointer[i];
						cmp.X[i] = data_s[i].X[pos];
						cmp.Y[i] = data_s[i].Y[pos];
						pointer[i] ++;

						if(cmp.X[i]>cmp.X[4])
							flag[i]=1;
						else if(cmp.X[i]==cmp.X[4]){
							index[i] = 1;
							joinnum ++;
						}
						else
							continue;
					}
				}
				write_data_blk(compare, cmp);

				for(i=0; i<=3; i++){
					if(!flag[i]&&index[i]==1){
						if(outnum<=2){
							out[0].X[outnum*2] = cmp.X[4];
							out[0].Y[outnum*2] = cmp.Y[4];
							out[0].X[outnum*2+1] = cmp.X[i];
							out[0].Y[outnum*2+1] = cmp.Y[i];
						}
						else if(outnum==3){
							out[0].X[6] = cmp.X[4];
							out[0].Y[6] = cmp.Y[4];
							out[1].X[0] = cmp.X[i];
							out[1].Y[0] = cmp.Y[i];
						}else{
							out[1].X[2*outnum-7] = cmp.X[4];
							out[1].Y[2*outnum-7] = cmp.Y[4];
							out[1].X[2*outnum-6] = cmp.X[i];
							out[1].Y[2*outnum-6] = cmp.Y[i];
						}
						outnum ++;
						//输出块写满了

						if(outnum==7){
							out[0].addr = addr+1;
							out[1].addr = addr+2;

							/*
							for(int m=0; m<7; m++){
								printf("%d %d\n", out[0].X[m], out[0].Y[m]);
							}
							printf("%d\n\n", out[0].addr);
							for(int m=0; m<7; m++){
								printf("%d %d\n", out[1].X[m], out[1].Y[m]);
							}
							printf("%d\n\n", out[1].addr);
							*/

							write_data_blk(output[0], out[0]);
							write_data_blk(output[1], out[1]);
							init_data_blk(&out[0]);
							init_data_blk(&out[1]);
							outnum = 0;
							writeBlockToDisk(output[0], addr, buf);
							printf("注：结果写入磁盘：%d\n", addr);
							writeBlockToDisk(output[1], addr+1, buf);
							printf("注：结果写入磁盘：%d\n", addr+1);
							//需要重新申请
							output[0] = getNewBlockInBuffer(buf);
                            output[1] = getNewBlockInBuffer(buf);
							addr += 2;
						}
					}
				}
			}
			for(i=0; i<4; i++){
                freeBlockInBuffer(blk_s[i], buf);
            }
		}
		freeBlockInBuffer(blk_r, buf);
		init_data_blk(&data_r);
	}
	out[0].addr = 0;
	/*
	for(int m=0; m<7; m++){
        printf("%d %d\n", out[0].X[m], out[0].Y[m]);
    }
    printf("%d\n\n", out[0].addr);
	*/

    write_data_blk(output[0], out[0]);
    writeBlockToDisk(output[0], addr, buf);
    printf("注：结果写入磁盘：563\n\n");

	printf("总共连接%d次\n\n", joinnum);
	freeBlockInBuffer(output[0], buf);
	freeBlockInBuffer(output[1], buf);
	freeBlockInBuffer(compare, buf);
	freeBlockInBuffer(blk_r, buf);

    return 0;
}


int func6(Buffer *buf){
	printf("------------------------------------------------------------\n");
    printf("基于排序的集合的交算法\n");
    printf("------------------------------------------------------------\n");
	unsigned char *blk_r, *compare;
	unsigned char *output;
	unsigned char *blk_s[4];
	int i, j, k;
	int group[4]; //S每组已经走了多少块
	int flag[4];	//遍历完毕置为1，遍历没完置为0
	int pointer[4];	//目前在哪个元组
	/*for(i=0; i<4; i++){
		flag[i] = 0;
		pointer[i] = 0;
	}*/
	data_blk data_s[4];
	/*for(i=0; i<4; i++){
		blk_s[i] = readBlockFromDisk(117+i*8, buf);
		group[i] = 1;
	}*/
	compare = getNewBlockInBuffer(buf);
	output = getNewBlockInBuffer(buf);
	data_blk data_r, cmp;
	data_blk out;
	int outnum = 0;	//记录输出块已经记录了多少个数了
	init_data_blk(&data_r);
	init_data_blk(&cmp);
	init_data_blk(&out);
	int addr = 601;
	int internum = 0;


	for(i=0; i<4; i++){
		init_data_blk(&data_s[i]);
	}
	for(k=301; k<=316; k++){
		blk_r = readBlockFromDisk(k, buf);
		read_data_blk(blk_r, &data_r);

		for (j=0; j<7; j++){
			cmp.X[4] = data_r.X[j];
			if(data_r.X[j]<=19)
				continue;

			cmp.Y[4] = data_r.Y[j];

			for(i=0; i<4; i++){
				flag[i] = 0;
				pointer[i] = 0;
			}
			//data_blk data_s[4];
			for(i=0; i<4; i++){
				blk_s[i] = readBlockFromDisk(117+i*8, buf);
				group[i] = 1;
			}
            //比较块中的比较
			while(!flag[0]||!flag[1]||!flag[2]||!flag[3]){
                //比较块的一次比完
				//一个块读完了，需要换块
				for(i=0; i<4; i++){
					if(pointer[i]==7){
						if (group[i]<8){
							freeBlockInBuffer(blk_s[i], buf);
							blk_s[i] = readBlockFromDisk(i*8+group[i]+117, buf);
							pointer[i] = 0;
						}
						group[i]++;
					}
				}

				//读完了一个组的所有块当然置为1
				for(i=0; i<4; i++){
					if(group[i]>8)
						flag[i]=1;
				}

				int index[4];
				for(i=0; i<=3; i++){
					index[i] = -1;
				}
				for(i=0; i<=3; i++){
					if(!flag[i]){
						read_data_blk(blk_s[i], &data_s[i]);
						int pos = pointer[i];
						cmp.X[i] = data_s[i].X[pos];
						cmp.Y[i] = data_s[i].Y[pos];
						pointer[i] ++;

						if(cmp.X[i]>cmp.X[4])
							flag[i]=1;
						else if(cmp.X[i]==cmp.X[4]&&cmp.Y[i]==cmp.Y[4]){
							index[i] = 1;
							internum ++;
						}
						else
							continue;
					}
				}
				write_data_blk(compare, cmp);

				for(i=0; i<=3; i++){
					if(!flag[i]&&index[i]==1){
						out.X[outnum] = cmp.X[4];
						out.Y[outnum] = cmp.Y[4];
						outnum ++;
						//输出块写满了

						if(outnum==7){
							out.addr = addr+1;

							for(int m=0; m<7; m++){
								printf("(X=%d,Y=%d)\n", out.X[m], out.Y[m]);
							}

							write_data_blk(output, out);
							init_data_blk(&out);
							outnum = 0;
							writeBlockToDisk(output, addr, buf);
							printf("注：结果写入磁盘：%d\n", addr);
							//需要重新申请
							output = getNewBlockInBuffer(buf);
							addr += 1;
						}
					}
				}
			}
			for(i=0; i<4; i++){
                freeBlockInBuffer(blk_s[i], buf);
            }
		}
		freeBlockInBuffer(blk_r, buf);
		init_data_blk(&data_r);
	}

	out.addr = 0;
	for(int m=0; m<outnum; m++){
        printf("(X=%d,Y=%d)\n", out.X[m], out.Y[m]);
    }
    write_data_blk(output, out);
    writeBlockToDisk(output, addr, buf);
    printf("注：结果写入磁盘：%d\n\n", addr);

	printf("S和R的交集有%d个元组\n\n", internum);
	freeBlockInBuffer(output, buf);
	freeBlockInBuffer(compare, buf);
	freeBlockInBuffer(blk_r, buf);
    return 0;
}


int func7(Buffer *buf){
	printf("------------------------------------------------------------\n");
    printf("基于排序的集合的并算法\n");
    printf("------------------------------------------------------------\n");

	unsigned char *blk_r, *compare;
	unsigned char *output;
	unsigned char *blk_s[4];
	int i, j, k;
	data_blk data_s[4];
	int addr = 701;
	int unionnum = 0;
	for(i=0; i<4; i++){
		init_data_blk(&data_s[i]);
	}

	//初始化
	for(j=0; j<8; j++){
		for(i=0; i<4; i++){
			blk_s[i] = readBlockFromDisk(117+i*8+j, buf);
			read_data_blk(blk_s[i], &data_s[i]);
			for(int m=0; m<7; m++){
				printf("(X=%d,Y=%d)\n", data_s[i].X[m], data_s[i].Y[m]);
			}
			writeBlockToDisk(blk_s[i], addr, buf);
			printf("注：结果写入磁盘：%d\n", addr);
			addr++;
			unionnum+=7;
			freeBlockInBuffer(blk_s[i], buf);
		}
	}

	int group[4]; //S每组已经走了多少块
	int flag[4];	//遍历完毕置为1，遍历没完置为0
	int pointer[4];	//目前在哪个元组

	compare = getNewBlockInBuffer(buf);
	output = getNewBlockInBuffer(buf);
	data_blk data_r, cmp;
	data_blk out;
	int outnum = 0;	//记录输出块已经记录了多少个数了
	init_data_blk(&data_r);
	init_data_blk(&cmp);
	init_data_blk(&out);

	for(i=0; i<4; i++){
		init_data_blk(&data_s[i]);
	}
	for(k=301; k<=316; k++){
		blk_r = readBlockFromDisk(k, buf);
		read_data_blk(blk_r, &data_r);

		for (j=0; j<7; j++){
			cmp.X[4] = data_r.X[j];
			int hit = 0;
			if(data_r.X[j]<=19)
				hit = 0;
			cmp.Y[4] = data_r.Y[j];

			for(i=0; i<4; i++){
				flag[i] = 0;
				pointer[i] = 0;
			}
			//data_blk data_s[4];
			for(i=0; i<4; i++){
				blk_s[i] = readBlockFromDisk(117+i*8, buf);
				group[i] = 1;
			}
            //比较块中的比较
			while(!flag[0]||!flag[1]||!flag[2]||!flag[3]){
                //比较块的一次比完
				//一个块读完了，需要换块
				for(i=0; i<4; i++){
					if(pointer[i]==7){
						if (group[i]<8){
							freeBlockInBuffer(blk_s[i], buf);
							blk_s[i] = readBlockFromDisk(i*8+group[i]+117, buf);
							pointer[i] = 0;
						}
						group[i]++;
					}
				}

				//读完了一个组的所有块当然置为1
				for(i=0; i<4; i++){
					if(group[i]>8)
						flag[i]=1;
				}

				for(i=0; i<=3; i++){
					if(!flag[i]){
						read_data_blk(blk_s[i], &data_s[i]);
						int pos = pointer[i];
						cmp.X[i] = data_s[i].X[pos];
						cmp.Y[i] = data_s[i].Y[pos];
						pointer[i] ++;

						if(cmp.X[i]>cmp.X[4])
							flag[i]=1;
						else if(cmp.X[i]==cmp.X[4]&&cmp.Y[i]==cmp.Y[4]){
							hit = 1;
						}
						else
							continue;
					}
				}
				write_data_blk(compare, cmp);
			}
			for(i=0; i<4; i++){
                freeBlockInBuffer(blk_s[i], buf);
            }

			if(hit==0){
				unionnum++;
				out.X[outnum] = cmp.X[4];
				out.Y[outnum] = cmp.Y[4];
				outnum++;
				if(outnum==7){
					out.addr = addr+1;

					for(int m=0; m<7; m++){
						printf("(X=%d,Y=%d)\n", out.X[m], out.Y[m]);
					}

					write_data_blk(output, out);
					init_data_blk(&out);
					outnum = 0;
					writeBlockToDisk(output, addr, buf);
					printf("注：结果写入磁盘：%d\n", addr);
					//需要重新申请
					output = getNewBlockInBuffer(buf);
					addr += 1;
				}
			}
		}
		freeBlockInBuffer(blk_r, buf);
		init_data_blk(&data_r);
	}

	out.addr = 0;
	for(int m=0; m<outnum; m++){
        printf("(X=%d,Y=%d)\n", out.X[m], out.Y[m]);
    }
    write_data_blk(output, out);
    writeBlockToDisk(output, addr, buf);
    printf("注：结果写入磁盘：%d\n\n", addr);
	printf("S和R的并集有%d个元组\n\n", unionnum);
	freeBlockInBuffer(output, buf);
	freeBlockInBuffer(compare, buf);
	freeBlockInBuffer(blk_r, buf);
    return 0;
}


int func8(Buffer *buf){
	printf("------------------------------------------------------------\n");
    printf("基于排序的集合的差算法R-S\n");
    printf("------------------------------------------------------------\n");
	unsigned char *blk_r, *compare;
	unsigned char *output;
	unsigned char *blk_s[4];
	int i, j, k;
	int group[4]; //S每组已经走了多少块
	int flag[4];	//遍历完毕置为1，遍历没完置为0
	int pointer[4];	//目前在哪个元组
	/*for(i=0; i<4; i++){
		flag[i] = 0;
		pointer[i] = 0;
	}*/
	data_blk data_s[4];
	/*for(i=0; i<4; i++){
		blk_s[i] = readBlockFromDisk(117+i*8, buf);
		group[i] = 1;
	}*/
	compare = getNewBlockInBuffer(buf);
	output = getNewBlockInBuffer(buf);
	data_blk data_r, cmp;
	data_blk out;
	int outnum = 0;	//记录输出块已经记录了多少个数了
	init_data_blk(&data_r);
	init_data_blk(&cmp);
	init_data_blk(&out);
	int addr = 801;
	int diffnum = 0;

	for(i=0; i<4; i++){
		init_data_blk(&data_s[i]);
	}
	for(k=301; k<=316; k++){
		blk_r = readBlockFromDisk(k, buf);
		read_data_blk(blk_r, &data_r);

		for (j=0; j<7; j++){
			cmp.X[4] = data_r.X[j];
			int hit = 0;
			if(data_r.X[j]<=19)
				hit = 0;
			cmp.Y[4] = data_r.Y[j];

			for(i=0; i<4; i++){
				flag[i] = 0;
				pointer[i] = 0;
			}
			//data_blk data_s[4];
			for(i=0; i<4; i++){
				blk_s[i] = readBlockFromDisk(117+i*8, buf);
				group[i] = 1;
			}
            //比较块中的比较
			while(!flag[0]||!flag[1]||!flag[2]||!flag[3]){
                //比较块的一次比完
				//一个块读完了，需要换块
				for(i=0; i<4; i++){
					if(pointer[i]==7){
						if (group[i]<8){
							freeBlockInBuffer(blk_s[i], buf);
							blk_s[i] = readBlockFromDisk(i*8+group[i]+117, buf);
							pointer[i] = 0;
						}
						group[i]++;
					}
				}

				//读完了一个组的所有块当然置为1
				for(i=0; i<4; i++){
					if(group[i]>8)
						flag[i]=1;
				}

				for(i=0; i<=3; i++){
					if(!flag[i]){
						read_data_blk(blk_s[i], &data_s[i]);
						int pos = pointer[i];
						cmp.X[i] = data_s[i].X[pos];
						cmp.Y[i] = data_s[i].Y[pos];
						pointer[i] ++;

						if(cmp.X[i]>cmp.X[4])
							flag[i]=1;
						else if(cmp.X[i]==cmp.X[4]&&cmp.Y[i]==cmp.Y[4]){
							hit = 1;
						}
						else
							continue;
					}
				}
				write_data_blk(compare, cmp);
			}
			for(i=0; i<4; i++){
                freeBlockInBuffer(blk_s[i], buf);
            }

			if(hit==0){
				diffnum++;
				out.X[outnum] = cmp.X[4];
				out.Y[outnum] = cmp.Y[4];
				outnum++;
				if(outnum==7){
					out.addr = addr+1;
					for(int m=0; m<7; m++){
						printf("(X=%d,Y=%d)\n", out.X[m], out.Y[m]);
					}
					write_data_blk(output, out);
					init_data_blk(&out);
					outnum = 0;
					writeBlockToDisk(output, addr, buf);
					printf("注：结果写入磁盘：%d\n", addr);
					//需要重新申请
					output = getNewBlockInBuffer(buf);
					addr += 1;
				}
			}
		}
		freeBlockInBuffer(blk_r, buf);
		init_data_blk(&data_r);
	}

	out.addr = 0;
	for(int m=0; m<outnum; m++){
        printf("(X=%d,Y=%d)\n", out.X[m], out.Y[m]);
    }
    write_data_blk(output, out);
    writeBlockToDisk(output, addr, buf);
    printf("注：结果写入磁盘：%d\n\n", addr);
	printf("R-S有%d个元组\n\n", diffnum);
	freeBlockInBuffer(output, buf);
	freeBlockInBuffer(compare, buf);
	freeBlockInBuffer(blk_r, buf);
	return 0;
}


int main(int argc, char **argv)
{
    Buffer buf; /* A buffer */

    /* Initialize the buffer */
    if (!initBuffer(520, 64, &buf))
    {
        perror("Buffer Initialization Failed!\n");
        return -1;
    }

    while(1){
        int choice = menu();
        switch(choice)
        {
            case 1:
            {
				func1(&buf);
                continue;
            }
            case 2:
            {
                tpmms(&buf);
                continue;
            }
			case 3:
			{
				setindex(&buf);
				func3(&buf);
				continue;
			}
			case 4:
			{
				func4(&buf);
				continue;
			}
			case 5:
            {
                func5(&buf);
                continue;
            }
            case 6:
            {
                func6(&buf);
                continue;
            }
			case 7:
			{
				func7(&buf);
				continue;
			}
			case 8:
			{
				func8(&buf);
				continue;
			}
            case 0:
            {
                freeBuffer(&buf);
                return 0;
            }
            default:
                continue;
        }
    }

}

