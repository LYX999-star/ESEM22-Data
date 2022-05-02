import subprocess

def mojo(file_A, file_B):
    logs = subprocess.run(
        ['java', 'mojo.MoJo', file_A, file_B],  # java mojo.MoJo mojo/distra.rsf mojo/distrb.rsf
        cwd=r'E:\opensource\Indirect Dependency\indirect-dependency\subspace',
        stdout=subprocess.PIPE)
    cmd = 'java mojo.Mojo {} {}'.format(file_A, file_B)
    return logs.stdout.decode('utf-8')


if __name__ == "__main__":

    rsf_path = r'E:\opensource\Indirect Dependency\indirect-dependency\subspace\rsf'
    method_rsf_path = r'E:\opensource\Indirect Dependency\indirect-dependency\subspace\rsf\{}\{}.rsf'

    fout = open("A2A_Res.txt", "a")

    for project in ['caffe', 'keras', 'Theano', 'pytorch', 'tensorflow'][:]:
        method_rsf_paths = [method_rsf_path.format(method, project) for method in ['depends', 'history', 'semantic']]
        print(project, ":\t")

        len_paths = len(method_rsf_paths)
        for i in range(len_paths):
            for j in range(i + 1, len_paths):
                methoda = method_rsf_paths[i].split('\\')[-2]
                methodb = method_rsf_paths[j].split('\\')[-2]
                project = method_rsf_paths[j].split('\\')[-1].split('.')[-2]
                print('\t', methoda, methodb, mojo(method_rsf_paths[i], method_rsf_paths[j]))